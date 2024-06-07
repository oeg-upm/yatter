import setuptools
import argparse
import time
import sys

v_time = str(int(time.time()))

parser = argparse.ArgumentParser()
parser.add_argument('-k', help="Release type", dest="kind")
parsed, rest = parser.parse_known_args()
sys.argv = [sys.argv[0]] + rest


with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("../VERSION", "r") as fh:
    v = fh.read().replace("\n", "")
    vers_taged = v


with open("../requirements.txt") as r:
    requirements = list(filter(None, r.read().split("\n")[0:]))

setuptools.setup(
    name="yatter",
    version=vers_taged,
    author="David Chaves-Fraga",
    author_email="david.chaves@usc.es",
    license="Apache 2.0",
    description="A translator from YARRRML to RML mappings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/yatter",
    project_urls={
        'Source code': 'https://github.com/oeg-upm/yatter',
        'Issue tracker': 'https://github.com/oeg-upm/yatter/issues',
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        'Intended Audience :: Information Technology',
        "Topic :: Utilities",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    ],
    install_requires=requirements,
    python_requires='>=3.7',
)
