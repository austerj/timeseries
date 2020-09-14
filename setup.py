from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="timeseries-austerj",
    version="0.1",
    author="Johan Auster",
    author_email="johanauster@gmail.com",
    description="A package for time series built from the standard library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/austerj/timeseries",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
