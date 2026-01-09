#!/usr/bin/env python
"""
Setup script for STM32 MCP Documentation Server.

This file exists for backwards compatibility with older pip versions and
tools that don't fully support pyproject.toml (PEP 517/518).

All package configuration is in pyproject.toml. This file simply delegates
to setuptools which reads the configuration from there.

For modern installations, use:
    pip install -e .
    pip install -e ".[dev]"

For legacy installations:
    python setup.py install
    python setup.py develop
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
