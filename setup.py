from setuptools import setup, find_packages

setup(
    name="dragon-api-client",
    version="0.1.0",
    description="Python API Client and CLI for the Dragon REST Python API",
    license="MIT",
    license_files=("LICENSE",),
    author="Dragon Team",
    author_email="dragonhpc@hpe.com",
    url="https://github.com/DragonHPC/dragon-cloud-client",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=["requests", "PyYAML", "click"],
    entry_points={
        "console_scripts": [
            "dragon = dragon_api_client.cli:cli",
        ],
    },
)
