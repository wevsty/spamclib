#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import ssl
import time
import selectors


class SyncTcpClient(object):

    def __init__(self,
                 *,
                 host='localhost',
                 port=783,
                 timeout=60.0,
                 ssl_context=None
                 ):
        self.host = host
        self.port = port
        self.timeout = timeout
        # ssl.SSLContext
        self.ssl_context = ssl_context
        self.sock = None

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_ssl_context(self, context):
        self.ssl_context = context

    def set_blocking(self, b_block):
        self.sock.setblocking(b_block)

    @staticmethod
    def get_default_ssl_context():
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode(ssl.CERT_NONE)
        return ssl_context

    def create_connection(self):
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        if self.ssl_context == None:
            self.sock = sock
        else:
            self.sock = self.ssl_context.wrap_socket(sock)
        # self.sock.setblocking(False)
        return

    def connect(self):
        self.create_connection()

    def close(self):
        if self.sock != None:
            self.sock.close()
        self.sock = None

    def is_closed(self):
        if self.sock != None:
            return False
        return True

    def send(self, bytes_data):
        if isinstance(bytes_data, str):
            self.sock.sendall(bytes_data.encode('utf-8'))
        elif isinstance(bytes_data, bytes):
            self.sock.sendall(bytes_data)
        else:
            self.sock.sendall(bytes(bytes_data))
        pass

    def send_all(self, bytes_data):
        if isinstance(bytes_data, str):
            self.sock.sendall(bytes_data.encode('utf-8'))
        elif isinstance(bytes_data, bytes):
            self.sock.sendall(bytes_data)
        else:
            self.sock.sendall(bytes(bytes_data))
        pass

    def select_recv_callback(self, sock, recv_size=1024 * 32):
        bytes_data = sock.recv(recv_size)
        return bytes_data

    def select_recv(self, loop_sleep_second=0.25):
        bytes_recv = b''
        n_buffer_size = 1024 * 32
        b_loop = True
        b_sleep = True
        float_waited_time = 0.0
        selector = selectors.DefaultSelector()
        selector.register(self.sock, selectors.EVENT_READ, self.select_recv_callback)
        while b_loop:
            se_events = selector.select()
            for key, mask in se_events:
                callback = key.data
                callback_return = callback(key.fileobj, n_buffer_size)
                if callback_return:
                    bytes_recv += callback_return
                else:
                    b_loop = False
                    break
                if len(callback_return) == n_buffer_size:
                    b_sleep = False
                else:
                    b_sleep = True
            pass
            if b_loop and b_sleep:
                float_waited_time += loop_sleep_second
                if float_waited_time > self.timeout:
                    break
                time.sleep(loop_sleep_second)
        pass
        selector.unregister(self.sock)
        selector.close()
        return bytes_recv

    def select_recv_until(self, bytes_end_flag=b'\n', loop_sleep_second=0.25):
        bytes_recv = b''
        n_buffer_size = 1024 * 32
        b_loop = True
        b_sleep = True
        float_waited_time = 0.0
        selector = selectors.DefaultSelector()
        selector.register(self.sock, selectors.EVENT_READ, self.select_recv_callback)
        while b_loop:
            se_events = selector.select()
            for key, mask in se_events:
                callback = key.data
                callback_return = callback(key.fileobj, n_buffer_size)
                if callback_return:
                    bytes_recv += callback_return
                if callback_return.endswith(bytes_end_flag):
                    b_loop = False
                    b_sleep = False
                    break
                if len(callback_return) == n_buffer_size:
                    b_sleep = False
                else:
                    b_sleep = True
            pass
            if b_loop and b_sleep:
                float_waited_time += loop_sleep_second
                if float_waited_time > self.timeout:
                    break
                time.sleep(loop_sleep_second)
        pass
        selector.unregister(self.sock)
        selector.close()
        return bytes_recv

    def recv(self, recv_size=1024 * 32):
        return self.sock.recv(recv_size)

    def recv_until(self, bytes_end_flag=b'\n'):
        bytes_data = b''
        while True:
            bytes_recv_data = self.recv()
            bytes_data += bytes_recv_data
            if len(bytes_end_flag) == 0:
                if len(bytes_recv_data) == 0:
                    break
            else:
                if bytes_recv_data.endswith(bytes_end_flag) == True:
                    break
        return bytes_data


if __name__ == '__main__':
    pass
