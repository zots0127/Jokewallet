import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jokewallet",
    version="0.0.4",
    author="Jams Rich",
    author_email="zots0127@gmail.com",
    description="A simple bitcoin demo wallet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zots0127/Jokewallet",
    install_requires=
    [
        'ecdsa',
        'requests',
        'qrcode_terminal',
    ],
    keywords = "Bitcoin Wallet ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
