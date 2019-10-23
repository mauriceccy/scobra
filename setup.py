import setuptools
import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Better to write it in requirements.txt
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open ("README.md","r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="scobra",
    version="0.0.2",
    author="Maurice Cheung",
    author_email="maurice.cheung@yale-nus.edu.sg",
    description="Supplementary package for COBRApy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mauriceccy/scobra",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
