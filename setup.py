from setuptools import setup, find_packages

setup(
    name="moral_graph",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "tabulate>=0.8.0",
    ],
    python_requires=">=3.9",
)
