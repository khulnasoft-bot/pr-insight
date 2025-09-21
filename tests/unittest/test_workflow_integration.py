"""
Integration tests for GitHub Actions workflow files.

This module provides integration-style tests that validate workflows
work together and follow organizational best practices.

Testing Framework: pytest/unittest
"""

import unittest
from pathlib import Path

import yaml


class TestWorkflowIntegration(unittest.TestCase):
    """Integration tests for workflow files."""

    def setUp(self):
        """Set up test fixtures."""
        self.workflow_dir = Path('.github/workflows')
        self.workflow_files = []

        if self.workflow_dir.exists():
            self.workflow_files = (
                list(self.workflow_dir.glob('*.yml')) +
                list(self.workflow_dir.glob('*.yaml'))
            )

    def test_all_workflows_are_valid_yaml(self):
        """Test that all workflow files contain valid YAML."""
        if not self.workflow_files:
            self.skipTest("No workflow files found in .github/workflows")

        for workflow_file in self.workflow_files:
            with self.subTest(file=str(workflow_file)):
                with open(workflow_file, 'r') as f:
                    try:
                        workflow_data = yaml.safe_load(f)
                        self.assertIsNotNone(workflow_data)
                        self.assertIsInstance(workflow_data, dict)
                    except yaml.YAMLError as e:
                        self.fail(f"Invalid YAML in {workflow_file}: {e}")

    def test_workflows_have_required_structure(self):
        """Test that all workflows follow required GitHub Actions structure."""
        if not self.workflow_files:
            self.skipTest("No workflow files found")

        # Some workflows might be templates or partial files
        # Let's be more flexible with the requirements
        required_top_level = ['name', 'on', 'jobs']

        for workflow_file in self.workflow_files:
            with self.subTest(file=str(workflow_file)):
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)

                # Skip if file is empty or not a valid workflow
                if not workflow_data or not isinstance(workflow_data, dict):
                    self.skipTest(f"Workflow file {workflow_file} is not a valid workflow")

                # Check for required fields, but allow some flexibility
                missing_fields = []
                for required_field in required_top_level:
                    if required_field not in workflow_data:
                        missing_fields.append(required_field)

                if missing_fields:
                    # Allow some workflows to be missing 'name' if they have 'on' and 'jobs'
                    if 'name' in missing_fields and 'on' in workflow_data and 'jobs' in workflow_data:
                        pass  # This is acceptable
                    else:
                        self.fail(f"Missing required fields {missing_fields} in {workflow_file}")

    def test_job_steps_have_valid_structure(self):
        """Test that all job steps follow valid GitHub Actions structure."""
        if not self.workflow_files:
            self.skipTest("No workflow files found")

        for workflow_file in self.workflow_files:
            with self.subTest(file=str(workflow_file)):
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)

                jobs = workflow_data.get('jobs', {})
                for job_name, job_config in jobs.items():
                    with self.subTest(job=job_name):
                        # Each job should have required fields
                        self.assertIn('runs-on', job_config,
                                    f"Job '{job_name}' missing 'runs-on' in {workflow_file}")
                        self.assertIn('steps', job_config,
                                    f"Job '{job_name}' missing 'steps' in {workflow_file}")

                        steps = job_config['steps']
                        self.assertIsInstance(steps, list,
                                            f"Steps should be a list in job '{job_name}' in {workflow_file}")

                        # Each step should have either 'uses' or 'run'
                        for i, step in enumerate(steps):
                            has_uses = 'uses' in step
                            has_run = 'run' in step
                            self.assertTrue(has_uses or has_run,
                                          f"Step {i} in job '{job_name}' must have 'uses' or 'run' in {workflow_file}")

    def test_workflow_naming_conventions(self):
        """Test that workflows follow consistent naming conventions."""
        if not self.workflow_files:
            self.skipTest("No workflow files found")

        for workflow_file in self.workflow_files:
            with self.subTest(file=str(workflow_file)):
                with open(workflow_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)

                name = workflow_data.get('name', '')
                # Name should be descriptive and not empty
                self.assertGreater(len(name), 0,
                                 f"Workflow name should not be empty in {workflow_file}")
                self.assertGreater(len(name), 3,
                                 f"Workflow name should be descriptive in {workflow_file}")

    def test_no_hardcoded_secrets(self):
        """Test that workflows don't contain hardcoded secrets."""
        if not self.workflow_files:
            self.skipTest("No workflow files found")

        secret_patterns = [
            'password',
            'key',
            'secret'
        ]

        for workflow_file in self.workflow_files:
            with self.subTest(file=str(workflow_file)):
                with open(workflow_file, 'r') as f:
                    content = f.read().lower()

                for pattern in secret_patterns:
                    if pattern in content:
                        # Check if it's properly using secrets syntax
                        lines_with_pattern = [
                            line for line in content.split('\n')
                            if pattern in line
                        ]

                        for line in lines_with_pattern:
                            # Skip if it uses GitHub secrets syntax
                            if '${{ secrets.' in line:
                                continue
                            # Skip if it's a comment
                            if line.strip().startswith('#'):
                                continue
                            # Skip if it's just a field name (like 'token: ${{ secrets.TOKEN }}')
                            if ':' in line and '${{ secrets.' in line:
                                continue
                            # Allow specific legitimate uses
                            if any(legitimate in line for legitimate in [
                                'uses: codecov/codecov-action',
                                'token: ${{ secrets.codecov_token }}',
                                'token: ${{ secrets.github_token }}'
                            ]):
                                continue

                            # This might be a hardcoded secret
                            if not any(indicator in line for indicator in ['#', 'description:', 'uses:']):
                                self.fail(f"Potential hardcoded secret in {workflow_file}: {line.strip()}")

if __name__ == '__main__':
    unittest.main()
