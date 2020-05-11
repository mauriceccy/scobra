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
    version="0.1.4",
    license='MIT',
    author="Maurice Cheung",
    author_email="maurice.cheung@yale-nus.edu.sg",
    description="Supplementary package for COBRApy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mauriceccy/scobra",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[ #find list of classifiers here https://pypi.org/classifiers/
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Science/Research',      # Define your audience
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',   # license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',     
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.5',
)
