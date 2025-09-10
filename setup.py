#!/usr/bin/env python3
"""
EDITO Workshops - Setup Script
Comprehensive resources and hands-on tutorials for contributing to the European Digital Twin of the Ocean (EDITO) platform.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="edito-workshops-presentations",
    version="0.1.0",
    author="EDITO Infrastructure Team",
    author_email="edito-infra-dev@mercator-ocean.eu",
    description="Comprehensive resources and hands-on tutorials for contributing to the European Digital Twin of the Ocean (EDITO) platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/EDITO-Infra/edito-workshops-presentations",
    project_urls={
        "Bug Reports": "https://github.com/EDITO-Infra/edito-workshops-presentations/issues",
        "Source": "https://github.com/EDITO-Infra/edito-workshops-presentations",
        "Documentation": "https://edito-infra.github.io/edito-workshops-presentations/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: R",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Documentation",
        "Topic :: Education",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "r": [
            "rpy2>=3.5.0",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.md",
            "*.yml",
            "*.yaml",
            "*.toml",
            "*.sh",
            "*.R",
            "*.Rmd",
            "*.ipynb",
            "docs/**/*",
            "using_datalab/**/*",
            "explore_data/**/*",
            "add_service/**/*",
            "add_tutorial/**/*",
            "data/**/*",
        ],
    },
    entry_points={
        "console_scripts": [
            "edito-workshop=edito_workshops.cli:main",
        ],
    },
    keywords=[
        "edito",
        "marine",
        "ocean", 
        "data",
        "tutorial",
        "workshop",
        "stac",
        "parquet",
        "zarr",
        "biodiversity",
        "oceanographic",
        "datalab",
        "rstudio",
        "jupyter",
        "vscode",
    ],
    zip_safe=False,
)
