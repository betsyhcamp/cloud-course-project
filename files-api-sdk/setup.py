# coding: utf-8

"""
    Files API

     ![Maintained by](https://img.shields.io/badge/Maintained_by-E_Camp-blue)   [Project Github Repo](https://github.com/betsyhcamp/cloud-course-project) 

    The version of the OpenAPI document: v0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "files-api-sdk"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil",
    "pydantic >= 1.10.5, < 2",
    "aenum"
]

setup(
    name=NAME,
    version=VERSION,
    description="Files API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Files API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
     ![Maintained by](https://img.shields.io/badge/Maintained_by-E_Camp-blue)   [Project Github Repo](https://github.com/betsyhcamp/cloud-course-project) 
    """,  # noqa: E501
    package_data={"files_api_sdk": ["py.typed"]},
)
