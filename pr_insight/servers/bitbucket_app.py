import asyncio
import base64
import copy
import hashlib
import json
import os
import re
import time
from collections import defaultdict
from typing import Dict, List, Optional

import jwt
import requests
import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response
from starlette.background import BackgroundTasks
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware

from pr_insight.agent.pr_insight import PRInsight
from pr_insight.algo.utils import update_settings_from_args
from pr_insight.config_loader import get_settings, global_settings
from pr_insight.git_providers.utils import apply_repo_settings
from pr_insight.identity_providers import get_identity_provider
from pr_insight.identity_providers.identity_provider import Eligibility
from pr_insight.log import LoggingFormat, get_logger, setup_logger
from pr_insight.secret_providers import get_secret_provider

setup_logger(fmt=LoggingFormat.JSON, level=get_settings().get("CONFIG.LOG_LEVEL", "DEBUG"))
router = APIRouter()
secret_provider = get_secret_provider() if get_settings().get("CONFIG.SECRET_PROVIDER") else None

# Rate limiting for Bitbucket webhooks
rate_limit_store: Dict[str, List[float]] = defaultdict(list)


def is_repo_allowed(repo_url: str) -> bool:
    """Check if a repository is in the allow-list."""
    allowed_repos = get_settings().get("CONFIG.BITBUCKET_ALLOWED_REPOS", [])

    if not allowed_repos:
        # If no allow-list is configured, allow all repos
        return True

    # Normalize repo URL for comparison
    normalized_url = repo_url.strip().rstrip('/').lower()

    for allowed_repo in allowed_repos:
        allowed_normalized = allowed_repo.strip().rstrip('/').lower()

        # Check for exact match
        if normalized_url == allowed_normalized:
            return True

        # Check for partial match (e.g., just project name)
        if normalized_url.endswith('/' + allowed_normalized) or \
           normalized_url.endswith('/' + allowed_normalized.split('/')[-1]):
            return True

        # Check for organization/project format
        if f"/{allowed_normalized}" in normalized_url:
            return True

    get_logger().warning(f"Repository {repo_url} not in allow-list")
    return False


def check_rate_limit(client_ip: str) -> bool:
    """Check if client IP is within rate limits."""
    now = time.time()
    max_per_minute = get_settings().get("CONFIG.BITBUCKET_RATE_LIMIT_PER_MINUTE", 60)

    # Clean old entries (older than 1 minute)
    rate_limit_store[client_ip] = [
        ts for ts in rate_limit_store[client_ip]
        if now - ts < 60
    ]

    if len(rate_limit_store[client_ip]) >= max_per_minute:
        get_logger().warning(f"Rate limit exceeded for IP {client_ip}")
        return False

    # Add current timestamp
    rate_limit_store[client_ip].append(now)
    return True


def check_concurrent_limit() -> bool:
    """Check if we're within concurrent webhook limits."""
    max_concurrent = get_settings().get("CONFIG.BITBUCKET_MAX_CONCURRENT_WEBHOOKS", 10)
    current_concurrent = len([task for task in asyncio.all_tasks() if "webhook" in str(task)])
    return current_concurrent < max_concurrent


async def get_bearer_token(shared_secret: str, client_key: str):
    try:
        now = int(time.time())
        url = "https://bitbucket.org/site/oauth2/access_token"
        canonical_url = "GET&/site/oauth2/access_token&"
        qsh = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()
        app_key = get_settings().bitbucket.app_key

        payload = {
            "iss": app_key,
            "iat": now,
            "exp": now + 240,
            "qsh": qsh,
            "sub": client_key,
        }
        token = jwt.encode(payload, shared_secret, algorithm="HS256")
        payload = "grant_type=urn%3Abitbucket%3Aoauth2%3Ajwt"
        headers = {"Authorization": f"JWT {token}", "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, headers=headers, data=payload)
        bearer_token = response.json()["access_token"]
        return bearer_token
    except Exception as e:
        get_logger().error(f"Failed to get bearer token: {e}")
        raise e


@router.get("/")
async def handle_manifest(request: Request, response: Response):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    manifest = open(os.path.join(cur_dir, "atlassian-connect.json"), "rt").read()
    try:
        manifest = manifest.replace("app_key", get_settings().bitbucket.app_key)
        manifest = manifest.replace("base_url", get_settings().bitbucket.base_url)
    except:
        get_logger().error("Failed to replace api_key in Bitbucket manifest, trying to continue")
    manifest_obj = json.loads(manifest)
    return JSONResponse(manifest_obj)


def _get_username(data):
    actor = data.get("data", {}).get("actor", {})
    if actor:
        if "username" in actor:
            return actor["username"]
        elif "display_name" in actor:
            return actor["display_name"]
        elif "nickname" in actor:
            return actor["nickname"]
    return ""


async def _perform_commands_bitbucket(
    commands_conf: str, agent: PRInsight, api_url: str, log_context: dict, data: dict
):
    apply_repo_settings(api_url)
    if (
        commands_conf == "pr_commands" and get_settings().config.disable_auto_feedback
    ):  # auto commands for PR, and auto feedback is disabled
        get_logger().info(f"Auto feedback is disabled, skipping auto commands for PR {api_url=}")
        return
    if data.get("event", "") == "pullrequest:created":
        if not should_process_pr_logic(data):
            return
    commands = get_settings().get(f"bitbucket_app.{commands_conf}", {})
    get_settings().set("config.is_auto_command", True)
    for command in commands:
        try:
            split_command = command.split(" ")
            command = split_command[0]
            args = split_command[1:]
            other_args = update_settings_from_args(args)
            new_command = " ".join([command] + other_args)
            get_logger().info(f"Performing command: {new_command}")
            with get_logger().contextualize(**log_context):
                await agent.handle_request(api_url, new_command)
        except Exception as e:
            get_logger().error(f"Failed to perform command {command}: {e}")


def is_bot_user(data) -> bool:
    try:
        actor = data.get("data", {}).get("actor", {})
        # allow actor type: user . if it's "AppUser" or "team" then it is a bot user
        allowed_actor_types = {"user"}
        if actor and actor["type"].lower() not in allowed_actor_types:
            get_logger().info(f"BitBucket actor type is not 'user', skipping: {actor}")
            return True
    except Exception as e:
        get_logger().error(f"Failed 'is_bot_user' logic: {e}")
    return False


def should_process_pr_logic(data) -> bool:
    try:
        pr_data = data.get("data", {}).get("pullrequest", {})
        title = pr_data.get("title", "")
        source_branch = pr_data.get("source", {}).get("branch", {}).get("name", "")
        target_branch = pr_data.get("destination", {}).get("branch", {}).get("name", "")
        sender = _get_username(data)

        # logic to ignore PRs from specific users
        ignore_pr_users = get_settings().get("CONFIG.IGNORE_PR_AUTHORS", [])
        if ignore_pr_users and sender:
            if sender in ignore_pr_users:
                get_logger().info(f"Ignoring PR from user '{sender}' due to 'config.ignore_pr_authors' setting")
                return False

        # logic to ignore PRs with specific titles
        if title:
            ignore_pr_title_re = get_settings().get("CONFIG.IGNORE_PR_TITLE", [])
            if not isinstance(ignore_pr_title_re, list):
                ignore_pr_title_re = [ignore_pr_title_re]
            if ignore_pr_title_re and any(re.search(regex, title) for regex in ignore_pr_title_re):
                get_logger().info(f"Ignoring PR with title '{title}' due to config.ignore_pr_title setting")
                return False

        ignore_pr_source_branches = get_settings().get("CONFIG.IGNORE_PR_SOURCE_BRANCHES", [])
        ignore_pr_target_branches = get_settings().get("CONFIG.IGNORE_PR_TARGET_BRANCHES", [])
        if ignore_pr_source_branches or ignore_pr_target_branches:
            if any(re.search(regex, source_branch) for regex in ignore_pr_source_branches):
                get_logger().info(
                    f"Ignoring PR with source branch '{source_branch}' due to config.ignore_pr_source_branches settings"
                )
                return False
            if any(re.search(regex, target_branch) for regex in ignore_pr_target_branches):
                get_logger().info(
                    f"Ignoring PR with target branch '{target_branch}' due to config.ignore_pr_target_branches settings"
                )
                return False
    except Exception as e:
        get_logger().error(f"Failed 'should_process_pr_logic': {e}")
    return True


@router.post("/webhook")
async def handle_github_webhooks(background_tasks: BackgroundTasks, request: Request):
    app_name = get_settings().get("CONFIG.APP_NAME", "Unknown")
    log_context = {"server_type": "bitbucket_app", "app_name": app_name}

    # Get client IP for rate limiting
    client_ip = request.client.host if request.client else "unknown"
    log_context["client_ip"] = client_ip

    # Rate limiting check
    if not check_rate_limit(client_ip):
        get_logger().warning(f"Rate limit exceeded for IP {client_ip}, rejecting webhook")
        return JSONResponse({"error": "Rate limit exceeded"}, status_code=429)

    # Concurrent limit check
    if not check_concurrent_limit():
        get_logger().warning(f"Concurrent webhook limit reached, queuing request")
        # Still process but log the warning

    get_logger().debug(request.headers)
    jwt_header = request.headers.get("authorization", None)
    if jwt_header:
        input_jwt = jwt_header.split(" ")[1]
    data = await request.json()
    get_logger().debug(data)

    async def inner():
        try:
            # ignore bot users
            if is_bot_user(data):
                return "OK"

            # Check if the PR should be processed
            if data.get("event", "") == "pullrequest:created":
                if not should_process_pr_logic(data):
                    return "OK"

            # Get the username of the sender
            log_context["sender"] = _get_username(data)

            sender_id = data.get("data", {}).get("actor", {}).get("account_id", "")
            log_context["sender_id"] = sender_id
            jwt_parts = input_jwt.split(".")
            claim_part = jwt_parts[1]
            claim_part += "=" * (-len(claim_part) % 4)
            decoded_claims = base64.urlsafe_b64decode(claim_part)
            claims = json.loads(decoded_claims)
            client_key = claims["iss"]
            secrets = json.loads(secret_provider.get_secret(client_key))
            shared_secret = secrets["shared_secret"]
            jwt.decode(input_jwt, shared_secret, audience=client_key, algorithms=["HS256"])
            bearer_token = await get_bearer_token(shared_secret, client_key)
            context["bitbucket_bearer_token"] = bearer_token
            context["settings"] = copy.deepcopy(global_settings)
            event = data["event"]
            agent = PRInsight()
            if event == "pullrequest:created":
                pr_url = data["data"]["pullrequest"]["links"]["html"]["href"]
                log_context["api_url"] = pr_url
                log_context["event"] = "pull_request"

                # Check if repository is in allow-list
                if not is_repo_allowed(pr_url):
                    get_logger().warning(f"Repository {pr_url} not in allow-list, ignoring webhook")
                    return "OK"

                if pr_url:
                    with get_logger().contextualize(**log_context):
                        apply_repo_settings(pr_url)
                        if (
                            get_identity_provider().verify_eligibility("bitbucket", sender_id, pr_url)
                            is not Eligibility.NOT_ELIGIBLE
                        ):
                            if get_settings().get("bitbucket_app.pr_commands"):
                                await _perform_commands_bitbucket("pr_commands", PRInsight(), pr_url, log_context, data)
            elif event == "pullrequest:comment_created":
                pr_url = data["data"]["pullrequest"]["links"]["html"]["href"]
                log_context["api_url"] = pr_url
                log_context["event"] = "comment"

                # Check if repository is in allow-list
                if not is_repo_allowed(pr_url):
                    get_logger().warning(f"Repository {pr_url} not in allow-list, ignoring webhook")
                    return "OK"

                comment_body = data["data"]["comment"]["content"]["raw"]
                with get_logger().contextualize(**log_context):
                    if (
                        get_identity_provider().verify_eligibility("bitbucket", sender_id, pr_url)
                        is not Eligibility.NOT_ELIGIBLE
                    ):
                        await agent.handle_request(pr_url, comment_body)
        except Exception as e:
            get_logger().error(f"Failed to handle webhook: {e}")

    background_tasks.add_task(inner)
    return "OK"


@router.get("/webhook")
async def handle_github_webhooks(request: Request, response: Response):
    return "Webhook server online!"


@router.post("/installed")
async def handle_installed_webhooks(request: Request, response: Response):
    try:
        get_logger().info("handle_installed_webhooks")
        get_logger().info(request.headers)
        data = await request.json()
        get_logger().info(data)
        shared_secret = data["sharedSecret"]
        client_key = data["clientKey"]
        username = data["principal"]["username"]
        secrets = {"shared_secret": shared_secret, "client_key": client_key}
        secret_provider.store_secret(username, json.dumps(secrets))
    except Exception as e:
        get_logger().error(f"Failed to register user: {e}")
        return JSONResponse({"error": "Unable to register user"}, status_code=500)


@router.post("/uninstalled")
async def handle_uninstalled_webhooks(request: Request, response: Response):
    get_logger().info("handle_uninstalled_webhooks")

    data = await request.json()
    get_logger().info(data)


def start():
    get_settings().set("CONFIG.PUBLISH_OUTPUT_PROGRESS", False)
    get_settings().set("CONFIG.GIT_PROVIDER", "bitbucket")
    get_settings().set("PR_DESCRIPTION.PUBLISH_DESCRIPTION_AS_COMMENT", True)
    middleware = [Middleware(RawContextMiddleware)]
    app = FastAPI(middleware=middleware)
    app.include_router(router)

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "3000")))


if __name__ == "__main__":
    start()
