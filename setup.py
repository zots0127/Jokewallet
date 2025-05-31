import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jokewallet",
    version="0.0.5",
    author="Jams Rich",
    author_email="zots0127@gmail.com",
    description="A simple bitcoin demo wallet with enhanced security and error handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zots0127/Jokewallet",
    install_requires=[
        'ecdsa>=0.17.0',
        'requests>=2.25.0',
        'qrcode_terminal>=0.8.0',
        'base58>=2.1.0',
    ],
    keywords="Bitcoin Wallet Cryptocurrency",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.7",
)
