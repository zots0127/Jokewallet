import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jokewallet",
    version="0.0.1",
    author="Jams Rich",
    author_email="zots0127@gmail.com",
    description="A simple bitcoin demo wallet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zots0127/Jokewallet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
