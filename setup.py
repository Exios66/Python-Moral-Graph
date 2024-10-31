from setuptools import setup, find_packages
from pathlib import Path

# Read README.md safely
readme_path = Path("README.md")
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="moral-graph",
    version="0.1.0",
    description="A psychology experiment simulator for evaluating AI chatbot interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com", 
    url="https://github.com/yourusername/moral-graph",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "moral_graph": [
            "templates/*.html",
            "templates/*.j2",
            "static/css/*.css",
            "static/js/*.js",
            "static/img/*"
        ],
    },
    install_requires=[
        "flask>=2.0.1,<3.0.0",
        "flask-cors>=3.0.10,<4.0.0",
        "pandas>=1.24.0,<2.0.0",
        "numpy>=1.24.0,<2.0.0",
        "python-dotenv>=0.19.0,<1.0.0",
        "tabulate>=0.8.9,<1.0.0",
        "scikit-learn>=1.0.2,<2.0.0",
        "matplotlib>=3.4.3,<4.0.0", 
        "seaborn>=0.11.2,<1.0.0",
        "plotly>=5.3.1,<6.0.0",
        "dash>=2.0.0,<3.0.0",
        "gunicorn>=20.1.0,<21.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5,<7.0.0",
            "pytest-cov>=2.12.1,<3.0.0",
            "black>=21.9b0,<22.0.0",
            "flake8>=3.9.2,<4.0.0",
            "mypy>=0.910,<1.0.0",
            "isort>=5.9.3,<6.0.0",
            "pre-commit>=2.15.0,<3.0.0"
        ],
        "docs": [
            "sphinx>=4.2.0,<5.0.0",
            "sphinx-rtd-theme>=1.0.0,<2.0.0", 
            "myst-parser>=0.15.2,<1.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "moral-graph=moral_graph.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Psychology"
    ],
    python_requires=">=3.9,<3.11",
    license="MIT",
    platforms=["any"],
    keywords=["psychology", "experiment", "simulation", "ai", "chatbot", "ethics"],
    zip_safe=False
)
