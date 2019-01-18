#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .type_convert import anything_to_string
from .type_convert import anything_to_bytes

from .spamc_header import SpamcHeader
from .spamc_body import SpamcBody


class SpamcProtocol(SpamcHeader, SpamcBody):
    def __init__(self):
        super().__init__()

    def create_request(self):
        request_body = b''
        if self.is_have_header(b'Compress') == True:
            request_body = self.zlib_compress_data(self.body)
        else:
            request_body = self.body
        self.set_content_length(len(request_body))

        request = (
            b'%(headers)b\r\n'
            b'%(body)b'
        )

        return request % {
            b'headers': self.create_header_request(),
            b'body': self.body
        }

    def create_simple_request(self, input_method, input_message):
        self.set_method(input_method)
        self.body = input_message
        return self.create_request()

    @staticmethod
    def split_spamd_message(input_message):
        try:
            bytes_header, sep, bytes_body = input_message.partition(b'\r\n\r\n')
            return bytes_header, bytes_body
        except Exception as err:
            raise RuntimeError('Protocol Error')

    def load_from_response(self, input_message):
        bytes_header, bytes_body = self.split_spamd_message(input_message)
        self.parse_header_bytes(bytes_header)
        if self.get_content_length() != len(bytes_body):
            return False
        if self.is_have_header(b'Compress') == True:
            response_body = self.zlib_decompress_data(bytes_body)
        else:
            response_body = bytes_body
        self.body = response_body
        return True

    def is_full_response(self, input_message, is_check_length=True):
        if input_message.startswith(b'SPAMD') == False:
            raise RuntimeError('Protocol Error')
        try:
            bytes_header, bytes_body = self.split_spamd_message(input_message)
            self.parse_header_bytes(bytes_header)
            if is_check_length == True:
                if self.is_have_header(b'Content-length') == False:
                    return False
                if self.get_content_length() != len(bytes_body):
                    return False
            return True
        except Exception as err:
            return False



if __name__ == '__main__':
    pass
