#!/usr/bin/env python3
"""
Run all tests with optional coverage.

Usage:
    python scripts/run_tests.py                    # Run all tests
    python scripts/run_tests.py --coverage         # Run with coverage report
    python scripts/run_tests.py --verbose          # Verbose output
    python scripts/run_tests.py --unit             # Run only unit tests
    python scripts/run_tests.py --integration      # Run only integration tests
    python scripts/run_tests.py --fast             # Skip slow tests
    python scripts/run_tests.py tests/test_chunking.py  # Run specific file
"""

import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run_tests(
    test_path: str = None,
    verbose: bool = False,
    coverage: bool = False,
    unit_only: bool = False,
    integration_only: bool = False,
    fast: bool = False,
    stop_on_first: bool = True,
    extra_args: list = None
) -> int:
    """
    Run pytest with the specified options.

    Args:
        test_path: Specific test file or directory to run
        verbose: Enable verbose output
        coverage: Generate coverage report
        unit_only: Run only unit tests (exclude integration)
        integration_only: Run only integration tests
        fast: Skip slow tests
        stop_on_first: Stop on first failure
        extra_args: Additional pytest arguments

    Returns:
        Exit code from pytest
    """
    # Build command
    cmd = [sys.executable, "-m", "pytest"]

    # Test path
    if test_path:
        cmd.append(test_path)
    elif unit_only:
        cmd.extend([
            str(PROJECT_ROOT / "tests" / "test_chunking.py"),
            str(PROJECT_ROOT / "tests" / "test_storage.py"),
            str(PROJECT_ROOT / "tests" / "test_mcp_tools.py"),
        ])
    elif integration_only:
        cmd.append(str(PROJECT_ROOT / "tests" / "test_integration.py"))
    else:
        cmd.append(str(PROJECT_ROOT / "tests"))

    # Verbose output
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("--tb=short")

    # Stop on first failure
    if stop_on_first:
        cmd.append("-x")

    # Skip slow tests
    if fast:
        cmd.extend(["-m", "not slow"])

    # Coverage
    if coverage:
        cmd.extend([
            "--cov=mcp_server",
            "--cov=pipeline",
            "--cov=storage",
            "--cov-report=term-missing",
            "--cov-report=html:coverage_html",
        ])

    # Extra arguments
    if extra_args:
        cmd.extend(extra_args)

    # Print command
    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)

    # Run tests
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    # Summary
    print("-" * 60)
    if result.returncode == 0:
        print("All tests passed!")
        if coverage:
            print(f"Coverage report: {PROJECT_ROOT / 'coverage_html' / 'index.html'}")
    else:
        print(f"Tests failed with exit code: {result.returncode}")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run STM32 MCP Documentation System tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/run_tests.py                    # Run all tests
    python scripts/run_tests.py --coverage         # Run with coverage
    python scripts/run_tests.py -v                 # Verbose output
    python scripts/run_tests.py --unit             # Unit tests only
    python scripts/run_tests.py --integration      # Integration tests only
    python scripts/run_tests.py --fast             # Skip slow tests
    python scripts/run_tests.py tests/test_chunking.py  # Specific file
        """
    )

    parser.add_argument(
        "test_path",
        nargs="?",
        default=None,
        help="Specific test file or directory to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose test output"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip slow tests"
    )
    parser.add_argument(
        "--no-stop",
        action="store_true",
        help="Don't stop on first failure"
    )
    parser.add_argument(
        "extra",
        nargs="*",
        help="Additional pytest arguments"
    )

    args = parser.parse_args()

    return run_tests(
        test_path=args.test_path,
        verbose=args.verbose,
        coverage=args.coverage,
        unit_only=args.unit,
        integration_only=args.integration,
        fast=args.fast,
        stop_on_first=not args.no_stop,
        extra_args=args.extra if args.extra else None
    )


if __name__ == "__main__":
    sys.exit(main())
