#!/usr/bin/env python3
"""
Test runner script for the QuickPick Multi-Agent System.
"""
import sys
import subprocess
import argparse
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Run a command and return success status.
    
    Args:
        command: Command to run
        description: Description of the command
    
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def install_test_dependencies():
    """Install test dependencies."""
    print("Installing test dependencies...")
    
    # Check if we're in a virtual environment
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Not in a virtual environment")
        print("Consider activating your virtual environment first")
    
    # Install test dependencies
    commands = [
        "pip install pytest pytest-asyncio pytest-cov pytest-mock",
        "pip install httpx fastapi[all]"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Installing: {cmd}"):
            return False
    
    return True


def run_unit_tests(verbose: bool = False, coverage: bool = False):
    """Run unit tests."""
    cmd = "pytest tests/unit/"
    
    if verbose:
        cmd += " -v"
    
    if coverage:
        cmd += " --cov=agents --cov=master --cov=mcp --cov-report=html --cov-report=term"
    
    return run_command(cmd, "Unit Tests")


def run_integration_tests(verbose: bool = False):
    """Run integration tests."""
    cmd = "pytest tests/integration/"
    
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "Integration Tests")


def run_e2e_tests(verbose: bool = False):
    """Run end-to-end tests."""
    cmd = "pytest tests/e2e/"
    
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "End-to-End Tests")


def run_all_tests(verbose: bool = False, coverage: bool = False):
    """Run all tests."""
    cmd = "pytest tests/"
    
    if verbose:
        cmd += " -v"
    
    if coverage:
        cmd += " --cov=agents --cov=master --cov=mcp --cov-report=html --cov-report=term"
    
    return run_command(cmd, "All Tests")


def run_specific_test(test_path: str, verbose: bool = False):
    """Run a specific test file or test function."""
    cmd = f"pytest {test_path}"
    
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, f"Specific Test: {test_path}")


def run_tests_with_markers(markers: str, verbose: bool = False):
    """Run tests with specific markers."""
    cmd = f"pytest -m {markers}"
    
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, f"Tests with markers: {markers}")


def lint_code():
    """Run code linting."""
    commands = [
        "flake8 agents/ master/ mcp/ --max-line-length=100 --ignore=E203,W503",
        "black --check agents/ master/ mcp/",
        "isort --check-only agents/ master/ mcp/"
    ]
    
    success = True
    for cmd in commands:
        if not run_command(cmd, f"Linting: {cmd}"):
            success = False
    
    return success


def format_code():
    """Format code."""
    commands = [
        "black agents/ master/ mcp/",
        "isort agents/ master/ mcp/"
    ]
    
    success = True
    for cmd in commands:
        if not run_command(cmd, f"Formatting: {cmd}"):
            success = False
    
    return success


def check_types():
    """Run type checking."""
    return run_command("mypy agents/ master/ mcp/ --ignore-missing-imports", "Type Checking")


def generate_test_report():
    """Generate comprehensive test report."""
    print("\n" + "="*60)
    print("GENERATING COMPREHENSIVE TEST REPORT")
    print("="*60)
    
    # Run tests with coverage
    cmd = "pytest tests/ --cov=agents --cov=master --cov=mcp --cov-report=html --cov-report=term-missing --cov-report=xml -v"
    
    if run_command(cmd, "Test Report Generation"):
        print("\n📊 Test report generated successfully!")
        print("📁 HTML coverage report: htmlcov/index.html")
        print("📄 XML coverage report: coverage.xml")
        return True
    else:
        print("\n❌ Test report generation failed")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="QuickPick Test Runner")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--test", type=str, help="Run specific test file or function")
    parser.add_argument("--markers", type=str, help="Run tests with specific markers")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--lint", action="store_true", help="Run code linting")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--types", action="store_true", help="Run type checking")
    parser.add_argument("--report", action="store_true", help="Generate test report")
    parser.add_argument("--ci", action="store_true", help="Run CI pipeline (all checks)")
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🚀 QuickPick Test Runner")
    print(f"📁 Working directory: {os.getcwd()}")
    
    success = True
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_test_dependencies():
            success = False
    
    # Run specific test types
    if args.unit:
        if not run_unit_tests(args.verbose, args.coverage):
            success = False
    
    if args.integration:
        if not run_integration_tests(args.verbose):
            success = False
    
    if args.e2e:
        if not run_e2e_tests(args.verbose):
            success = False
    
    if args.all:
        if not run_all_tests(args.verbose, args.coverage):
            success = False
    
    if args.test:
        if not run_specific_test(args.test, args.verbose):
            success = False
    
    if args.markers:
        if not run_tests_with_markers(args.markers, args.verbose):
            success = False
    
    # Code quality checks
    if args.lint:
        if not lint_code():
            success = False
    
    if args.format:
        if not format_code():
            success = False
    
    if args.types:
        if not check_types():
            success = False
    
    if args.report:
        if not generate_test_report():
            success = False
    
    # CI pipeline
    if args.ci:
        print("\n🔄 Running CI Pipeline...")
        ci_commands = [
            ("pytest tests/ --cov=agents --cov=master --cov=mcp --cov-report=term-missing", "Tests with Coverage"),
            ("flake8 agents/ master/ mcp/ --max-line-length=100 --ignore=E203,W503", "Code Linting"),
            ("black --check agents/ master/ mcp/", "Code Formatting Check"),
            ("isort --check-only agents/ master/ mcp/", "Import Sorting Check"),
            ("mypy agents/ master/ mcp/ --ignore-missing-imports", "Type Checking")
        ]
        
        for cmd, description in ci_commands:
            if not run_command(cmd, description):
                success = False
    
    # If no specific command was given, run all tests
    if not any([args.unit, args.integration, args.e2e, args.all, args.test, 
                args.markers, args.lint, args.format, args.types, args.report, args.ci]):
        print("\n📋 No specific command given, running all tests...")
        if not run_all_tests(args.verbose, args.coverage):
            success = False
    
    # Final result
    print("\n" + "="*60)
    if success:
        print("🎉 All operations completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some operations failed. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
