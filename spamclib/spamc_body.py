#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .type_convert import anything_to_string
from .type_convert import anything_to_bytes
import zlib


class SpamcBody(object):
    _body = b''
    # _compressed_body = b''

    def __init__(self):
        self._body = b''
        # self._compressed_body = b''

    @staticmethod
    def format_body(input_body):
        return_body = anything_to_bytes(input_body)
        if return_body.endswith(b'\n') == True:
            return return_body
        else:
            return return_body + b'\n'

    # body函数可当成属性使用
    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = self.format_body(value)

    @staticmethod
    def zlib_compress_data(value):
        return zlib.compress(value)

    @staticmethod
    def zlib_decompress_data(value):
        return zlib.decompress(value)


if __name__ == '__main__':
    pass
