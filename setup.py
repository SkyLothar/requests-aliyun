# -*- coding: utf-8 -*-

import os
import sys

from codecs import open

__version__ = "0.2.5"
__author__ = "SkyLothar"
__email__ = "allothar@gmail.com"
__url__ = "http://github.com/skylothar/requests-aliyun"


try:
    import setuptools
except ImportError:
    from distutils.core import setuptools


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


packages = ["aliyunauth"]


with open("README.rst", "r", "utf-8") as f:
    readme = f.read()

with open("requirements.txt", "r", "utf-8") as f:
    requires = f.read()

with open("tests/requirements.txt", "r", "utf-8") as f:
    tests_require = f.read()


setuptools.setup(
    name="requests-aliyun",
    version=__version__,
    description="authentication for aliyun service",
    long_description=readme,
    author=__author__,
    author_email=__email__,
    url=__url__,
    packages=packages,
    package_data={
        "": ["LICENSE"]
    },
    package_dir={
        "aliyunauth": "aliyunauth"
    },
    include_package_data=True,
    install_requires=requires,
    license="Apache 2.0",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
    setup_requires=["nose >= 1.0"],
    tests_require=tests_require,
    test_suite="nose.collector"
)
