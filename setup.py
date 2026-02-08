"""
CoHumAIn Framework Setup
Collective Human and Machine Intelligence for Explainable Multi-Agent Systems
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()
requirements = [req for req in requirements if req and not req.startswith("#")]

setup(
    name="cohumain",
    version="1.0.0",
    author="Himanshu Joshi, Shivani Shukla",
    author_email="info@cohumain.ai",
    description="Explainable Multi-Agent Systems Framework with Safe Human Collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration",
    project_urls={
        "Bug Tracker": "https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration/issues",
        "Documentation": "https://cohumain.ai/docs",
        "Source Code": "https://github.com/HimJoe/CoHumAIn-A-Framework-for-Explainable-Multi-Agent-Systems-with-Safe-Human-Collaboration",
        "Paper": "https://github.com/CoHumAInLabs/CoHumAIn-Framework/blob/main/paper/cohumain_paper.pdf",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.0",
            "mkdocstrings[python]>=0.24.0",
        ],
        "all": [
            "redis>=5.0.1",
            "prometheus-client>=0.19.0",
            "psycopg2-binary>=2.9.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "cohumain=cohumain.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cohumain": [
            "configs/*.yaml",
            "configs/**/*.yaml",
        ],
    },
    keywords=[
        "explainable ai",
        "multi-agent systems",
        "ai safety",
        "human-ai collaboration",
        "transparency",
        "xai",
        "regulated industries",
        "finance",
        "healthcare",
        "compliance",
    ],
    zip_safe=False,
)
