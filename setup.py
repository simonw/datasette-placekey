import os

from setuptools import setup

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-placekey",
    description="SQL functions for working with placekeys",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-placekey",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-placekey/issues",
        "CI": "https://github.com/simonw/datasette-placekey/actions",
        "Changelog": "https://github.com/simonw/datasette-placekey/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_placekey"],
    entry_points={"datasette": ["placekey = datasette_placekey"]},
    install_requires=["datasette", "placekey"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-placekey[test]"],
    python_requires=">=3.6",
)
