#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .type_convert import anything_to_string
from .type_convert import anything_to_bytes


class SpamcHeader(object):
    method = b''
    protocol_version = b'1.5'
    status_code = 0
    status_message = b'EX_OK'
    header_dict = {}

    def __init__(self):
        self.method = b''
        self.protocol_version = b'1.5'
        self.status_code = 0
        self.status_message = b'EX_OK'
        self.header_dict = {}

    def set_method(self, input_method):
        self.method = anything_to_bytes(input_method)

    def set_header(self, input_bytes_key, input_bytes_value):
        bytes_key = anything_to_bytes(input_bytes_key)
        bytes_value = anything_to_bytes(input_bytes_value)
        self.header_dict[bytes_key] = bytes_value

    def get_header(self, input_bytes_key):
        return self.header_dict.get(input_bytes_key, b'')

    def delete_header(self, input_bytes_key):
        bytes_key = anything_to_bytes(input_bytes_key)
        self.header_dict.pop(bytes_key, None)

    def set_content_length(self, input_number):
        if isinstance(input_number, int):
            self.set_header(b'Content-length', input_number)
        else:
            self.set_header(b'Content-length', int(input_number))

    def get_content_length(self):
        bytes_len = self.get_header(b'Content-length')
        if len(bytes_len) == 0:
            return 0
        return int(bytes_len)

    def is_have_header(self, input_bytes_key):
        return input_bytes_key in self.header_dict

    def create_header_argv(self):
        line_list = []
        for bytes_key, bytes_value in self.header_dict.items():
            bytes_line = b'%s: %s\r\n' % (bytes_key, bytes_value)
            line_list.append(bytes_line)
        bytes_header_argv = b''.join(line_list)
        return bytes_header_argv

    def create_header_request(self):
        request = (
            b'%(method)b SPAMC/%(version)b\r\n'
            b'%(headers)b'
        )

        return request % {
            b'method': self.method,
            b'version': self.protocol_version,
            b'headers': self.create_header_argv()
        }

    def parse_header_flag_version(self, bytes_flag):
        # spamd_flag,sep,spamd_ver=b"SPAMD/1.1".partition(b'/')
        spamd_flag, sep, spamd_ver = bytes_flag.partition(b'/')
        if spamd_flag != b'SPAMD':
            raise RuntimeError('Protocol Error')
        self.protocol_version = spamd_ver

    def parse_header_status_code(self, bytes_status_code):
        self.status_code = int(bytes_status_code)

    def parse_header_status_message(self, bytes_status_message):
        self.status_message = bytes_status_message

    def parse_header_first_line(self, bytes_line_data):
        # b'SPAMD/1.1 0 EX_OK'.split(b' ', 2) -> [b'SPAMD/1.1', b'0', b'EX_OK']
        # b'SPAMD/1.0 76 Bad header line: (Content-Length contains non-numeric bytes)'
        try:
            spamd_flag, spamd_status_code, spamd_status_message = bytes_line_data.split(b' ', 2)
            self.parse_header_flag_version(spamd_flag)
            self.parse_header_status_code(spamd_status_code)
            self.parse_header_status_message(spamd_status_message)
        except Exception as err:
            raise RuntimeError('Protocol Error')
        finally:
            pass

    def parse_header_line(self, bytes_line_data):
        try:
            header_key, sep, header_value = bytes_line_data.partition(b': ')
            self.header_dict[header_key] = header_value
        except Exception as err:
            raise RuntimeError('Protocol Error')
        finally:
            pass

    def parse_header_bytes(self, bytes_header):
        header_line_list = bytes_header.splitlines()
        for index in range(len(header_line_list)):
            bytes_line = header_line_list[index]
            if index == 0:
                self.parse_header_first_line(bytes_line)
            else:
                self.parse_header_line(bytes_line)




if __name__ == '__main__':
    pass
