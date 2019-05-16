import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zebuker-db",
    version="1.0.3",
    author="Zeel",
    author_email="engineering@zeel.com",
    description="Package to be used as source for DB models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeel-dev/zebuker-db",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[],
    python_requires='~=3.6',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ]
)