import argparse
import asyncio
import os
import sys
from typing import Optional, List
from pathlib import Path

from pr_insight.agent.pr_insight import PRInsight, commands
from pr_insight.algo.utils import get_version
from pr_insight.config_loader import get_settings
from pr_insight.log import get_logger, setup_logger

log_level = os.environ.get("LOG_LEVEL", "INFO")
setup_logger(log_level)


class CLIFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom formatter with better formatting for CLI help."""

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        else:
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return ', '.join(action.option_strings) + ' ' + args_string


class PRInsightCLI:
    """Enhanced CLI interface for PR-Insight."""

    def __init__(self):
        self.logger = get_logger()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser with subcommands."""
        parser = argparse.ArgumentParser(
            description="AI-based pull request analyzer and reviewer",
            formatter_class=CLIFormatter,
            epilog="""Examples:
    pr-insight pr review --pr-url https://github.com/user/repo/pull/123
    pr-insight pr describe --pr-url https://github.com/user/repo/pull/123
    pr-insight pr ask "What does this PR do?" --pr-url https://github.com/user/repo/pull/123
    pr-insight pr improve --pr-url https://github.com/user/repo/pull/123 --extended
    pr-insight config list
    pr-insight help review

💡 Tip: Try Groq models for faster inference! Run 'pr-insight config wizard' to set up Groq.
    """
        )
        parser.add_argument(
            "--version", action="version", version=f"pr-insight {get_version()}"
        )
        parser.add_argument(
            "--config", type=str, help="Path to configuration file"
        )
        parser.add_argument(
            "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO", help="Set logging level"
        )

        # Create subparsers for different command groups
        subparsers = parser.add_subparsers(dest='command_group', help='Command group')

        # PR Commands
        pr_parser = subparsers.add_parser(
            'pr', help='Pull request operations',
            formatter_class=CLIFormatter
        )
        pr_subparsers = pr_parser.add_subparsers(dest='pr_command', help='PR command')

        # Review command
        review_parser = pr_subparsers.add_parser(
            'review', help='Review a pull request',
            formatter_class=CLIFormatter
        )
        review_parser.add_argument('--pr-url', required=True, help='Pull request URL')
        review_parser.add_argument('--issue-url', help='Issue URL (alternative to PR URL)')
        review_parser.add_argument('--extended', action='store_true', help='Enable extended review mode')
        review_parser.add_argument('--extra-instructions', help='Additional review instructions')

        # Describe command
        describe_parser = pr_subparsers.add_parser(
            'describe', help='Generate PR description',
            formatter_class=CLIFormatter
        )
        describe_parser.add_argument('--pr-url', required=True, help='Pull request URL')
        describe_parser.add_argument('--inline-summary', action='store_true', help='Include inline file summaries')

        # Improve command
        improve_parser = pr_subparsers.add_parser(
            'improve', help='Suggest code improvements',
            formatter_class=CLIFormatter
        )
        improve_parser.add_argument('--pr-url', required=True, help='Pull request URL')
        improve_parser.add_argument('--extended', action='store_true', help='Enable extended improvement mode')

        # Ask command
        ask_parser = pr_subparsers.add_parser(
            'ask', help='Ask questions about a PR',
            formatter_class=CLIFormatter
        )
        ask_parser.add_argument('--pr-url', required=True, help='Pull request URL')
        ask_parser.add_argument('question', nargs='*', help='Question to ask about the PR')
        ask_parser.add_argument('--line-numbers', help='Specific line numbers to ask about')

        # Similar issue command
        similar_issue_parser = pr_subparsers.add_parser(
            'similar_issue', help='Find similar issues to the given PR/issue',
            formatter_class=CLIFormatter
        )
        similar_issue_parser.add_argument('--pr-url', help='Pull request URL')
        similar_issue_parser.add_argument('--issue-url', required=True, help='Issue URL (required)')

        # Configuration Commands
        config_parser = subparsers.add_parser(
            'config', help='Configuration management',
            formatter_class=CLIFormatter
        )
        config_subparsers = config_parser.add_subparsers(dest='config_command', help='Config command')

        config_list_parser = config_subparsers.add_parser('list', help='List current configuration')
        config_set_parser = config_subparsers.add_parser('set', help='Set configuration value')
        config_set_parser.add_argument('key', help='Configuration key')
        config_set_parser.add_argument('value', help='Configuration value')
        config_get_parser = config_subparsers.add_parser('get', help='Get configuration value')
        config_get_parser.add_argument('key', help='Configuration key')
        config_wizard_parser = config_subparsers.add_parser('wizard', help='Run interactive configuration wizard')

        # Help command
        help_parser = subparsers.add_parser('help', help='Show help for commands')
        help_parser.add_argument('topic', nargs='?', help='Specific command to get help for')

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI with given arguments."""
        parser = self.create_parser()

        if not args:
            args = sys.argv[1:]

        # Handle empty arguments
        if not args:
            parser.print_help()
            return 1

        parsed_args = parser.parse_args(args)

        # Update log level if specified
        if hasattr(parsed_args, 'log_level'):
            setup_logger(parsed_args.log_level)

        # Load configuration if specified
        if hasattr(parsed_args, 'config') and parsed_args.config:
            config_path = Path(parsed_args.config)
            if config_path.exists():
                get_settings().load_file(config_path)
            else:
                self.logger.error(f"Configuration file not found: {config_path}")
                return 1

        # Set CLI mode
        get_settings().set("CONFIG.CLI_MODE", True)

        try:
            return asyncio.run(self._execute_command(parsed_args))
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
            return 130
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return 1

    async def _execute_command(self, args: argparse.Namespace) -> int:
        """Execute the parsed command."""
        if not hasattr(args, 'command_group') or not args.command_group:
            self.create_parser().print_help()
            return 1

        if args.command_group == 'pr':
            return await self._execute_pr_command(args)
        elif args.command_group == 'config':
            return self._execute_config_command(args)
        elif args.command_group == 'help':
            return self._execute_help_command(args)
        else:
            self.logger.error(f"Unknown command group: {args.command_group}")
            return 1

    async def _execute_pr_command(self, args: argparse.Namespace) -> int:
        """Execute PR-related commands."""
        # Determine the URL to use
        url = getattr(args, 'pr_url', None) or getattr(args, 'issue_url', None)
        if not url:
            self.logger.error("No PR or issue URL provided")
            return 1

        # Build command arguments
        command_args = [args.pr_command]

        # Add additional arguments based on command
        if args.pr_command == 'review' and getattr(args, 'extended', False):
            command_args.append('--extended')
        elif args.pr_command == 'review' and getattr(args, 'extra_instructions', None):
            command_args.extend(['--extra_instructions', args.extra_instructions])
        elif args.pr_command == 'describe' and getattr(args, 'inline_summary', False):
            command_args.append('--inline_summary')
        elif args.pr_command == 'improve' and getattr(args, 'extended', False):
            command_args.append('--extended')
        elif args.pr_command == 'ask' and args.question:
            command_args.extend(args.question)
        elif args.pr_command == 'ask' and getattr(args, 'line_numbers', None):
            command_args.extend(['--line_numbers', args.line_numbers])

        # Execute the command
        result = await PRInsight().handle_request(url, command_args)
        return 0 if result else 1

    def _execute_config_command(self, args: argparse.Namespace) -> int:
        """Execute configuration commands."""
        if not hasattr(args, 'config_command') or not args.config_command:
            self.logger.error("No config command specified")
            return 1

        if args.config_command == 'list':
            # List current configuration
            settings = get_settings()
            print("Current configuration:")
            for key in sorted(settings.keys()):
                value = settings[key]
                if isinstance(value, (str, int, float, bool)):
                    print(f"  {key}: {value}")
        elif args.config_command == 'set':
            if not hasattr(args, 'key') or not hasattr(args, 'value'):
                self.logger.error("Both key and value must be specified for config set")
                return 1
            get_settings().set(args.key, args.value)
            print(f"Set {args.key} = {args.value}")
        elif args.config_command == 'get':
            if not hasattr(args, 'key'):
                self.logger.error("Key must be specified for config get")
                return 1
            value = get_settings().get(args.key)
            if value is not None:
                print(f"{args.key}: {value}")
            else:
                self.logger.error(f"Configuration key '{args.key}' not found")
                return 1
        elif args.config_command == 'wizard':
            return self._execute_config_wizard()

        return 0

    def _execute_config_wizard(self) -> int:
        """Execute configuration wizard."""
        try:
            from pr_insight.config_wizard import ConfigWizard
            wizard = ConfigWizard()
            wizard.run()
            return 0
        except ImportError as e:
            self.logger.error(f"Could not import configuration wizard: {e}")
            return 1
        except Exception as e:
            self.logger.error(f"Error running configuration wizard: {e}")
            return 1

    def _execute_help_command(self, args: argparse.Namespace) -> int:
        """Execute help commands."""
        if hasattr(args, 'topic') and args.topic:
            if args.topic in ['review', 'describe', 'improve', 'ask']:
                print(f"\nHelp for '{args.topic}' command:")
                print(getattr(self, f'_get_{args.topic}_help', lambda: "No help available")())
            else:
                print(f"\nNo help available for '{args.topic}'")
        else:
            self.create_parser().print_help()
        return 0

    def _get_review_help(self) -> str:
        """Get help text for review command."""
        return """
The 'review' command analyzes a pull request and provides:
- Summary of changes
- Specific suggestions for improvement
- Code quality assessment

Usage:
  pr-insight pr review --pr-url <URL> [options]

Options:
  --extended    Enable extended review mode for more thorough analysis
  --extra-instructions    Additional instructions for the reviewer

Example:
  pr-insight pr review --pr-url https://github.com/user/repo/pull/123 --extended
        """

    def _get_describe_help(self) -> str:
        """Get help text for describe command."""
        return """
The 'describe' command generates or updates the PR description based on:
- PR content analysis
- File changes summary
- Feature documentation

Usage:
  pr-insight pr describe --pr-url <URL> [options]

Options:
  --inline-summary    Include inline file summaries in the description

Example:
  pr-insight pr describe --pr-url https://github.com/user/repo/pull/123
        """

    def _get_improve_help(self) -> str:
        """Get help text for improve command."""
        return """
The 'improve' command suggests specific code improvements:
- Code quality improvements
- Best practice suggestions
- Bug fixes and optimizations

Usage:
  pr-insight pr improve --pr-url <URL> [options]

Options:
  --extended    Enable extended improvement mode for comprehensive analysis

Example:
  pr-insight pr improve --pr-url https://github.com/user/repo/pull/123 --extended
        """

    def _get_ask_help(self) -> str:
        """Get help text for ask command."""
        return """
The 'ask' command allows you to ask questions about specific aspects of a PR:
- General questions about the PR's purpose
- Questions about specific code sections
- Questions about implementation details

Usage:
  pr-insight pr ask <question> --pr-url <URL> [options]

Options:
  --line-numbers    Ask about specific line numbers

Examples:
  pr-insight pr ask "What does this PR do?" --pr-url https://github.com/user/repo/pull/123
  pr-insight pr ask "Review this function" --pr-url https://github.com/user/repo/pull/123 --line-numbers 10-25

💡 Tip: Groq models are optimized for fast inference and work great with this command!
        """


# Backward compatibility
class CLI:
    """Legacy CLI class for backward compatibility."""

    @staticmethod
    def set_parser():
        """Legacy method for backward compatibility."""
        cli = PRInsightCLI()
        return cli.create_parser()

    @staticmethod
    def run_command(pr_url, command):
        """Legacy method for backward compatibility."""
        cli = PRInsightCLI()
        args = ['pr', command.lstrip('/'), '--pr-url', pr_url]
        return cli.run(args)


def run():
    """Main entry point for the CLI."""
    cli = PRInsightCLI()
    exit_code = cli.run()
    return exit_code


if __name__ == "__main__":
    cli = PRInsightCLI()
    exit_code = cli.run()
    sys.exit(exit_code)
