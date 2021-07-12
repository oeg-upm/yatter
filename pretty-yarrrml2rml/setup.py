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
    if parsed.kind == "rel":
        vers_taged = v
    else:
        vers_taged = v+".dev"+v_time


with open("../requirements.txt") as r:
    requirements = list(filter(None, r.read().split("\n")[0:]))

setuptools.setup(
    name="pretty-yarrrml2rml",
    version=vers_taged,
    author="David Chaves-Fraga",
    author_email="david.chaves@upm.es",
    license="Apache 2.0",
    description="The tool translates mapping rules in RML from YARRRML serialization to RDF turtle in a pretty and interpreatable way for humans. The translation is based on RML and YARRRML specifications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/pretty-yarrrml2rml",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
