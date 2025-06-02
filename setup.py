#!/usr/bin/env python3
"""
Setup script for Professional LLM Evaluation Framework
A comprehensive tool for evaluating Large Language Models with beautiful HTML reports.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Professional LLM Evaluation Framework with beautiful HTML reports"

# Read version from __init__.py
def get_version():
    try:
        with open("llm_eval/__init__.py", "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "1.0.0"

# Read requirements
def read_requirements():
    requirements = []
    try:
        with open("requirements.txt", "r") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        # Fallback to essential requirements
        requirements = [
            "torch>=2.7.0",
            "transformers>=4.20.0",
            "numpy>=1.21.0",
            "pandas>=1.3.0",
            "tqdm>=4.62.0",
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0",
            "datasets>=2.0.0",
            "accelerate>=0.12.0",
            "sacrebleu>=2.0.0",
            "sqlitedict>=2.0.0",
            "lm-eval>=0.4.0",
        ]
    return requirements

setup(
    name="llm-testkit",
    version=get_version(),
    author="Matthias De Paolis",
    author_email="mattdepaolis@users.noreply.github.com",
    description="Professional LLM Evaluation Framework with Beautiful HTML Reports",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mattdepaolis/llm-eval",
    project_urls={
        "Bug Tracker": "https://github.com/mattdepaolis/llm-eval/issues",
        "Documentation": "https://github.com/mattdepaolis/llm-eval#readme",
        "Source Code": "https://github.com/mattdepaolis/llm-eval",
    },
    packages=find_packages(include=["llm_eval", "llm_eval.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
        "gpu": [
            "torch[cuda]",
            "accelerate[gpu]",
        ],
        "all": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "torch[cuda]",
            "accelerate[gpu]",
        ],
    },
    entry_points={
        "console_scripts": [
            "llm-eval=llm_eval.cli:main",
            "llm-eval-demo=llm_eval.cli:demo_main",
            "llm-eval-html=llm_eval.cli:html_main",
            "llm-eval-showcase=llm_eval.cli:showcase_main",
        ],
    },
    include_package_data=True,
    package_data={
        "llm_eval": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "configs/*.yaml",
            "configs/*.json",
        ],
    },
    zip_safe=False,
    keywords="llm evaluation language-models ai machine-learning nlp transformers",
    license="MIT",
) 