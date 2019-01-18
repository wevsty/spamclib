#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def anything_to_string(input_data):
    if isinstance(input_data, str):
        return input_data
    elif isinstance(input_data, bytes):
        # return input_data.decode('utf-8', 'ignore')
        return input_data.decode('utf-8')
    elif isinstance(input_data, int):
        return str(input_data)
    else:
        return input_data.__str__()
        # raise ValueError('Should be str or bytes object.')


def anything_to_bytes(input_data):
    if isinstance(input_data, str):
        # return input_data.encode('utf-8', 'ignore')
        return input_data.encode('utf-8')
    elif isinstance(input_data, bytes):
        return input_data
    elif isinstance(input_data, int):
        return str(input_data).encode('utf-8')
    else:
        return input_data.__bytes__()
        # raise ValueError('Should be str or bytes object.')


if __name__ == '__main__':
    pass
