# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from files_api_sdk.models.get_files_response import GetFilesResponse  # noqa: E501

class TestGetFilesResponse(unittest.TestCase):
    """GetFilesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetFilesResponse:
        """Test GetFilesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetFilesResponse`
        """
        model = GetFilesResponse()  # noqa: E501
        if include_optional:
            return GetFilesResponse(
                files = [
                    files_api_sdk.models.file_metadata.FileMetadata(
                        file_path = '', 
                        last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        size_bytes = 56, )
                    ],
                next_page_token = ''
            )
        else:
            return GetFilesResponse(
                files = [
                    files_api_sdk.models.file_metadata.FileMetadata(
                        file_path = '', 
                        last_modified = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        size_bytes = 56, )
                    ],
                next_page_token = '',
        )
        """

    def testGetFilesResponse(self):
        """Test GetFilesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
