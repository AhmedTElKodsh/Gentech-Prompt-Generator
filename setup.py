from setuptools import setup, find_packages

setup(
    name="promptgen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "altair",
    ],
    python_requires=">=3.8",
) 