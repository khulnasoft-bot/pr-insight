#!/usr/bin/env python3
"""
Simple test script to verify CLI structure without dependencies
"""
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, '/Users/dev/pr-insight')

def test_cli_structure():
    """Test the CLI structure without importing heavy dependencies."""
    print("Testing CLI structure...")

    # Test basic imports
    try:
        from pr_insight.cli import PRInsightCLI, CLIFormatter
        print("✅ CLI classes imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CLI classes: {e}")
        return False

    # Test parser creation
    try:
        cli = PRInsightCLI()
        parser = cli.create_parser()
        print("✅ Parser created successfully")
        print(f"   Parser description: {parser.description}")
    except Exception as e:
        print(f"❌ Failed to create parser: {e}")
        return False

    # Test help generation
    try:
        help_text = parser.format_help()
        print("✅ Help text generated successfully")
        print(f"   Help text length: {len(help_text)} characters")
    except Exception as e:
        print(f"❌ Failed to generate help text: {e}")
        return False

    # Test basic argument parsing
    try:
        test_args = ['pr', 'review', '--pr-url', 'https://github.com/test/repo/pull/1']
        args = parser.parse_args(test_args)
        print("✅ Arguments parsed successfully")
        print(f"   Command group: {args.command_group}")
        print(f"   PR command: {args.pr_command}")
        print(f"   PR URL: {args.pr_url}")
    except Exception as e:
        print(f"❌ Failed to parse arguments: {e}")
        return False

    print("\n🎉 CLI structure test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_cli_structure()
    sys.exit(0 if success else 1)
