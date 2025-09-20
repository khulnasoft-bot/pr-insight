#!/usr/bin/env python3
"""
Configuration setup wizard for PR-Insight CLI.
This script helps users configure PR-Insight for first use.
"""
import os
import sys
from pathlib import Path
from typing import Optional

# Add the parent directory to sys.path to import pr_insight modules
sys.path.insert(0, str(Path(__file__).parent))

from pr_insight.config_loader import get_settings


class ConfigWizard:
    """Interactive configuration wizard for PR-Insight."""

    def __init__(self):
        self.settings = get_settings()
        self.config_file = Path.home() / '.pr-insight.toml'
        self.config_data = {}
        self.model_config = None  # Will be set if Groq is selected

    def run(self):
        """Run the configuration wizard."""
        print("🔧 PR-Insight Configuration Wizard")
        print("=" * 40)

        if self.config_file.exists():
            print(f"⚠️  Configuration file already exists at {self.config_file}")
            if not self._confirm_overwrite():
                print("Configuration wizard cancelled.")
                return

        print("\nThis wizard will help you set up PR-Insight for your development workflow.")
        print("You'll need to provide some basic information to get started.")

        # Security Setup
        self._setup_security()

        # AI Provider Setup
        self._setup_ai_provider()

        # Save configuration
        self._save_config()

        print(f"\n✅ Configuration saved to {self.config_file}")
        print("\nYou can now use PR-Insight CLI:")
        print("  pr-insight pr review --pr-url https://github.com/user/repo/pull/123")

    def _setup_git_provider(self):
        """Setup Git provider configuration."""
        print("\n📋 Git Provider Setup")
        print("-" * 25)

        providers = ['github', 'gitlab', 'bitbucket', 'azure-devops']
        print("Supported Git providers:")
        for i, provider in enumerate(providers, 1):
            print(f"  {i}. {provider.title()}")

        while True:
            choice = input(f"\nWhich Git provider do you use? [1-{len(providers)}]: ").strip()
            try:
                provider_idx = int(choice) - 1
                if 0 <= provider_idx < len(providers):
                    git_provider = providers[provider_idx]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(providers)}")
            except ValueError:
                print("Please enter a valid number")

        print(f"Selected: {git_provider.title()}")

        # Get API credentials
        if git_provider == 'github':
            token = self._get_input_with_default("GitHub Personal Access Token", "GITHUB_TOKEN")
            if token:
                self.config_data['github'] = {'user_token': token}
        elif git_provider == 'gitlab':
            token = self._get_input_with_default("GitLab Personal Access Token", "GITLAB_TOKEN")
            if token:
                self.config_data['gitlab'] = {'private_token': token}
        elif git_provider == 'bitbucket':
            username = input("Bitbucket username: ").strip()
            app_password = self._get_input_with_default("Bitbucket App Password", "BITBUCKET_TOKEN")
            if username and app_password:
                self.config_data['bitbucket'] = {
                    'username': username,
                    'app_password': app_password
                }
        elif git_provider == 'azure-devops':
            org_url = input("Azure DevOps organization URL: ").strip()
            token = self._get_input_with_default("Azure DevOps Personal Access Token", "AZURE_DEVOPS_TOKEN")
            if org_url and token:
                self.config_data['azure_devops'] = {
                    'org_url': org_url,
                    'personal_access_token': token
                }

    def _setup_security(self):
        """Setup security configuration."""
        print("\n🔒 Security Setup")
        print("-" * 15)

        # Secret Provider Setup
        print("Secret storage options:")
        print("  1. Local file storage (recommended for development)")
        print("  2. Google Cloud Storage (recommended for production)")

        while True:
            choice = input("\nWhich secret storage provider would you like to use? [1-2] (default: 1): ").strip()
            if not choice:
                choice = "1"

            if choice == "1":
                self.config_data['secret_provider'] = 'local_file'
                secrets_dir = input("Secrets directory (default: ./secrets): ").strip()
                if secrets_dir:
                    self.config_data['secrets_dir'] = secrets_dir
                break
            elif choice == "2":
                self.config_data['secret_provider'] = 'google_cloud_storage'
                print("Note: You'll need to configure Google Cloud credentials separately.")
                break
            else:
                print("Please enter 1 or 2")

        # Bitbucket Security Setup
        print("\n🪣 Bitbucket Security Setup")
        print("-" * 25)

        enable_allowlist = input("Enable repository allow-list for Bitbucket webhooks? [Y/n]: ").strip().lower()
        if enable_allowlist in ['', 'y', 'yes']:
            print("\nEnter allowed repositories (one per line, empty line to finish):")
            print("Examples:")
            print("  https://bitbucket.org/company/project1")
            print("  project1")
            print("  company/project1")

            allowed_repos = []
            while True:
                repo = input("> ").strip()
                if not repo:
                    break
                allowed_repos.append(repo)

            if allowed_repos:
                self.config_data['bitbucket_allowed_repos'] = allowed_repos
                print(f"Added {len(allowed_repos)} repositories to allow-list")

        # Rate limiting setup
        rate_limit = input("Max webhooks per minute per IP (default: 60): ").strip()
        if rate_limit and rate_limit.isdigit():
            self.config_data['bitbucket_rate_limit_per_minute'] = int(rate_limit)

        # Concurrent webhook limit
        concurrent_limit = input("Max concurrent webhook processing (default: 10): ").strip()
        if concurrent_limit and concurrent_limit.isdigit():
            self.config_data['bitbucket_max_concurrent_webhooks'] = int(concurrent_limit)

    def _setup_ai_provider(self):
        """Setup AI provider configuration."""
        print("\n🤖 AI Provider Setup")
        print("-" * 20)

        providers = ['openai', 'anthropic', 'google', 'azure', 'groq']
        print("Supported AI providers:")
        for i, provider in enumerate(providers, 1):
            print(f"  {i}. {provider.title()}")

        while True:
            choice = input(f"\nWhich AI provider do you prefer? [1-{len(providers)}]: ").strip()
            try:
                provider_idx = int(choice) - 1
                if 0 <= provider_idx < len(providers):
                    ai_provider = providers[provider_idx]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(providers)}")
            except ValueError:
                print("Please enter a valid number")

        print(f"Selected: {ai_provider.title()}")

        # Get API key
        env_var_map = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'azure': 'AZURE_OPENAI_API_KEY',
            'groq': 'GROQ_API_KEY'
        }

        api_key = self._get_input_with_default(
            f"{ai_provider.title()} API Key",
            env_var_map.get(ai_provider, f"{ai_provider.upper()}_API_KEY")
        )

        if api_key:
            if ai_provider == 'openai':
                self.config_data['openai'] = {'key': api_key}
            elif ai_provider == 'anthropic':
                self.config_data['anthropic'] = {'key': api_key}
            elif ai_provider == 'google':
                self.config_data['google'] = {'key': api_key}
            elif ai_provider == 'azure':
                self.config_data['azure'] = {
                    'openai': {
                        'key': api_key,
                        'endpoint': input("Azure OpenAI endpoint (optional): ").strip() or None
                    }
                }
            elif ai_provider == 'groq':
                self.config_data['groq'] = {'key': api_key}

                # Ask which Groq model to use as default
                print("\n🦙 Groq Models Available:")
                groq_models = [
                    'llama3-8b-8192',
                    'llama3-70b-8192',
                    'llama3.1-8b-instant',
                    'llama3.1-70b-versatile',
                    'llama3.1-405b-reasoner',
                    'mixtral-8x7b-32768',
                    'gemma-7b-it',
                    'gemma2-9b-it'
                ]

                print("Recommended models:")
                for i, model in enumerate(groq_models[:4], 1):  # Show first 4 as recommended
                    print(f"  {i}. {model}")

                while True:
                    model_choice = input(f"\nWhich Groq model would you like to use? [1-{len(groq_models)}] (default: 2): ").strip()
                    if not model_choice:
                        selected_model = groq_models[1]  # Default to llama3-70b-8192
                        break
                    try:
                        model_idx = int(model_choice) - 1
                        if 0 <= model_idx < len(groq_models):
                            selected_model = groq_models[model_idx]
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(groq_models)}")
                    except ValueError:
                        print("Please enter a valid number")

                print(f"Selected model: {selected_model}")

                # Ask about fallback models
                fallback_input = input("Use OpenAI models as fallback? [Y/n]: ").strip().lower()
                if fallback_input in ['', 'y', 'yes']:
                    fallback_models = ["gpt-4o-2024-11-20", "gpt-4o-mini-2024-07-18"]
                    print(f"Will use {fallback_models} as fallback models")
                else:
                    fallback_models = []
                    print("No fallback models configured")

                # Set the model configuration
                self.model_config = {
                    'model': selected_model,
                    'fallback_models': fallback_models
                }

    def _get_input_with_default(self, prompt: str, env_var: str) -> Optional[str]:
        """Get input with environment variable as default."""
        env_value = os.environ.get(env_var)
        if env_value:
            use_env = input(f"{prompt} [from {env_var}]: ").strip()
            if not use_env:
                return env_value

        return input(f"{prompt}: ").strip() or None

    def _confirm_overwrite(self) -> bool:
        """Ask user if they want to overwrite existing config."""
        response = input("Do you want to continue and overwrite? [y/N]: ").strip().lower()
        return response in ['y', 'yes']

    def _save_config(self):
        """Save configuration to file."""
        import toml

        # Create directory if it doesn't exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w') as f:
            toml.dump(self.config_data, f)

        print(f"\n💡 Tip: You can also set these values as environment variables:")
        for key, value in self.config_data.items():
            if isinstance(value, dict) and 'key' in value:
                print(f"  export {key.upper()}_API_KEY=your_key_here")
            elif key == 'github' and 'user_token' in value:
                print("  export GITHUB_TOKEN=your_github_token_here")

        # If Groq was selected, show model information
        if self.model_config:
            print("\n🤖 Groq Model Configuration:")
            print(f"  Primary model: {self.model_config['model']}")
            if self.model_config['fallback_models']:
                print(f"  Fallback models: {', '.join(self.model_config['fallback_models'])}")
            print("\n💡 To use these models, add to your .pr-insight.toml or settings:")
            print(f"  [config]")
            print(f"  model=\"{self.model_config['model']}\"")
            if self.model_config['fallback_models']:
                print(f"  fallback_models={self.model_config['fallback_models']}")
            print("\n🦙 Groq models are optimized for speed and are great for fast code review!")

        # Show security configuration summary
        if 'secret_provider' in self.config_data:
            print("\n🔐 Security Configuration:")
            provider = self.config_data['secret_provider']
            print(f"  Secret provider: {provider}")
            if 'secrets_dir' in self.config_data:
                print(f"  Secrets directory: {self.config_data['secrets_dir']}")
            if 'bitbucket_allowed_repos' in self.config_data:
                print(f"  Bitbucket allow-list: {len(self.config_data['bitbucket_allowed_repos'])} repositories")
            if 'bitbucket_rate_limit_per_minute' in self.config_data:
                print(f"  Rate limit: {self.config_data['bitbucket_rate_limit_per_minute']} webhooks/minute")
            if 'bitbucket_max_concurrent_webhooks' in self.config_data:
                print(f"  Concurrent limit: {self.config_data['bitbucket_max_concurrent_webhooks']} simultaneous webhooks")


def main():
    """Main entry point."""
    wizard = ConfigWizard()
    try:
        wizard.run()
    except KeyboardInterrupt:
        print("\n\nConfiguration wizard cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during configuration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
