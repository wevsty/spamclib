#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import ssl
from .sync_tcp_client import SyncTcpClient
from .spamc_protocol import SpamcProtocol


class SyncSpamcClient(SyncTcpClient):

    def __init__(self,
                 *,
                 host='localhost',
                 port=783,
                 timeout=60.0,
                 ssl_context=None
                 ):
        super().__init__(
            host=host,
            port=port,
            timeout=timeout,
            ssl_context=ssl_context
        )
        pass

    def recv_full_data(self, is_check_length=True):
        return_response_object = SpamcProtocol()
        bytes_response_data = b''
        self.set_blocking(False)
        while True:
            bytes_recv_data = self.select_recv()
            bytes_response_data += bytes_recv_data
            if return_response_object.is_full_response(bytes_response_data, is_check_length) == True:
                break
        return bytes_response_data

    def command_ping(self):
        self.connect()
        self.send(b'PING SPAMC/1.5\r\n\r\n')
        bytes_response_data = self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_skip(self):
        self.connect()
        self.send(b'SKIP SPAMC/1.5\r\n\r\n')
        #bytes_response_data = self.recv_full_data()
        self.close()
        return None

    def command_check(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'CHECK', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_headers(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'HEADERS', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_process(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'PROCESS', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_report(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'REPORT', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_report_ifspam(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'REPORT_IFSPAM', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    def command_symbols(self, bytes_data):
        self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'SYMBOLS', bytes_data)
        self.send(bytes_request_data)
        bytes_response_data = self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object


if __name__ == '__main__':
    pass


