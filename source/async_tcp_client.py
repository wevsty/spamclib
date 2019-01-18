#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging


class AsyncTcpClient:

    def __init__(self,
                 *,
                 host='localhost',
                 port=783,
                 ssl=None,
                 loop=None
                 ):
        self._is_connected = False
        self.loop = loop or asyncio.get_event_loop()
        self.host = host
        self.port = port
        self.ssl = ssl
        self.logger = logging.getLogger(__name__)
        self.reader = None
        self.writer = None

    async def __aenter__(self):
        self.logger.debug('Connecting to %s', self.connection_string)
        self.reader, self.writer = await self.open()
        self._is_connected = True
        self.logger.debug('Connected to %s', self.connection_string)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug('Closing connection to %s', self.connection_string)
        self.close()
        self.logger.debug('Closed connection to %s', self.connection_string)

    async def open(self):
        try:
            reader, writer = await asyncio.open_connection(self.host,
                                                           self.port,
                                                           ssl=self.ssl,
                                                           loop=self.loop)
            self.reader = reader
            self.writer = writer
        except (ConnectionRefusedError, OSError) as error:
            self.logger.exception('Cannot connecting to %s:%s: %s',
                                  self.host,
                                  self.port,
                                  raised)
            raise error
        return None

    async def connect(self):
        await self.open()

    def close(self):
        self.writer.close()
        # await self.writer.wait_closed()
        self._is_connected = False
        self.reader = None
        self.writer = None

    async def send(self, data):
        self.writer.write(data)
        await self.writer.drain()

    # receive
    async def recv(self):
        return await self.reader.read()

    async def recv_until(self,bytes_sep=b'\n'):
        bytes_recv_data = b''
        while True:
            bytes_recv_data += await self.recv()
            if bytes_recv_data.endswith(bytes_sep):
                break
        return bytes_recv_data


if __name__ == '__main__':
    pass
