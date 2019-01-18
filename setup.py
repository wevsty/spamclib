#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages


def get_long_description():
    readme_path = Path(__file__).absolute().parent / 'README.md'
    with readme_path.open(encoding='utf-8') as fp:
        long_description = fp.read()
    return long_description


setup(
    name='spamclib',
    version='0.0.2',

    description='A SPAMC protocol library.'
                'Help you use SpamAssassin\'s SPAMD service.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    url='https://github.com/wevsty/spamclib',

    author='wevsty',
    author_email='ty@wevs.org',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: MIT License',

        'Topic :: Communications :: Email :: Filters',
        'Topic :: Software Development :: Libraries'
    ],

    keywords='spam spamc spamd spamassassin',

    packages=find_packages(),

    python_requires='>=3.6',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
)
