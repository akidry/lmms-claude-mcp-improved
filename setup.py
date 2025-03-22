#!/usr/bin/env python3
"""
Setup script for LMMS-Claude-MCP
"""

from setuptools import setup, find_packages

setup(
    name="lmms-mcp",
    version="0.1.0",
    description="LMMS integration with Claude AI through Model Context Protocol (MCP)",
    author="akidry",
    author_email="akidry@example.com",
    url="https://github.com/akidry/lmms-claude-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-osc>=1.8.0",
        "websockets>=10.0",
        "model-context-protocol>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "lmms-mcp=lmms_mcp.cli:main",
        ],
    },
)