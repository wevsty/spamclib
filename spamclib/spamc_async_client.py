#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .async_tcp_client import AsyncTcpClient
from .spamc_protocol import SpamcProtocol


class AsyncSpamcClient(AsyncTcpClient):

    def __init__(self,
                 *,
                 host='localhost',
                 port=783,
                 ssl=None,
                 loop=None
                 ):
        super().__init__(
            host=host,
            port=port,
            ssl=ssl,
            loop=loop
        )
        pass

    async def recv_full_data(self, is_check_length=True):
        return_response_object = SpamcProtocol()
        bytes_response_data = b''
        while True:
            bytes_recv_data = await self.recv()
            bytes_response_data += bytes_recv_data
            if return_response_object.is_full_response(bytes_response_data, is_check_length) == True:
                break
        return bytes_response_data

    async def command_ping(self):
        await self.connect()
        await self.send(b'PING SPAMC/1.5\r\n\r\n')
        bytes_response_data = await self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_skip(self):
        await self.connect()
        await self.send(b'SKIP SPAMC/1.5\r\n\r\n')
        #bytes_response_data = self.recv_full_data()
        self.close()
        return None

    async def command_check(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'CHECK', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_headers(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'HEADERS', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_process(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'PROCESS', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_report(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'REPORT', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_report_ifspam(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'REPORT_IFSPAM', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data()
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object

    async def command_symbols(self, bytes_data):
        await self.connect()
        request_object = SpamcProtocol()
        bytes_request_data = request_object.create_simple_request(b'SYMBOLS', bytes_data)
        await self.send(bytes_request_data)
        bytes_response_data = await self.recv_full_data(False)
        return_response_object = SpamcProtocol()
        return_response_object.load_from_response(bytes_response_data)
        self.close()
        return return_response_object


if __name__ == '__main__':
    pass


