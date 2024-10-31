from setuptools import setup, find_packages

setup(
    name="moral-graph",
    version="0.1.0",
    description="A psychology experiment simulator for evaluating AI chatbot interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/moral-graph",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/**/*"],
    },
    install_requires=[
        "flask>=2.0.1",
        "flask-cors>=3.0.10",
        "pandas>=1.24.0", 
        "numpy>=1.24.0",
        "pytest>=6.2.5",
        "python-dotenv>=0.19.0",
        "tabulate>=0.8.9",
        "scikit-learn>=1.0.2",
        "matplotlib>=3.4.3",
        "seaborn>=0.11.2",
        "plotly>=5.3.1",
        "dash>=2.0.0",
        "gunicorn>=20.1.0",
        "black>=21.9b0",
        "flake8>=3.9.2",
        "mypy>=0.910",
        "isort>=5.9.3"
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.1",
            "black>=21.9b0",
            "flake8>=3.9.2",
            "mypy>=0.910",
            "isort>=5.9.3",
            "pre-commit>=2.15.0"
        ],
        "docs": [
            "sphinx>=4.2.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.15.2"
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
    python_requires=">=3.9",
    license="MIT",
    platforms=["any"],
    keywords=["psychology", "experiment", "simulation", "ai", "chatbot", "ethics"],
)
