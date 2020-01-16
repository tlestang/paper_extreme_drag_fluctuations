import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jfm_paper", # Replace with your own username
    version="0.0.1",
    author="Thibault Lestang",
    author_email="thibault.lestang@cs.ox.ac.uk",
    description="A python package to reproduce the results of the jfm paper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/tlestang/jfm_paper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy>=1.16",
        "scipy>=1.0",
        "pandas>=0.23",
        "matplotlib>=2.0",
        ],
)
