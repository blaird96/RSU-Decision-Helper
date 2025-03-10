from setuptools import setup, find_packages

setup(
    name="RSUHelper",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "RSUHelper=RSUHelper.__main__:main"
        ]
    },
)
