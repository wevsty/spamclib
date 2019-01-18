#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio
from spamclib.spamc_async_client import AsyncSpamcClient

GTUBE = '''
Subject: Test spam mail (GTUBE)
Message-ID: <GTUBE1.1010101@example.net>
Date: Wed, 23 Jul 2003 23:30:00 +0200
From: Sender <sender@example.net>
To: Recipient <recipient@example.net>
Precedence: junk
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

This is the GTUBE, the
	Generic
	Test for
	Unsolicited
	Bulk
	Email

If your spam filter supports it, the GTUBE provides a test by which you
can verify that the filter is installed correctly and is detecting incoming
spam. You can send yourself a test mail containing the following string of
characters (in upper case and with no white spaces and line breaks):

XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X

You should send this test mail from an account outside of your network.

'''
bytes_GTUBE = GTUBE.encode('utf-8')
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    sc = AsyncSpamcClient(loop=loop)
    # ping cannot support SpamAssassinForWindows
    loop.run_until_complete(sc.command_ping())
    loop.run_until_complete(sc.command_skip())
    res = loop.run_until_complete(sc.command_check(bytes_GTUBE))
    print(res)
    print('Status code : %d' % res.status_code)
    print('Status message : %s' % res.status_message.decode('utf-8'))
    print('Header item Spam : %s' % res.get_header(b'Spam').decode('utf-8'))
    print('Response body : %s' % res.body.decode('utf-8'))
    loop.run_until_complete(sc.command_headers(bytes_GTUBE))
    loop.run_until_complete(sc.command_process(bytes_GTUBE))
    loop.run_until_complete(sc.command_report(bytes_GTUBE))
    loop.run_until_complete(sc.command_report_ifspam(bytes_GTUBE))
    loop.run_until_complete(sc.command_symbols(bytes_GTUBE))
    pass


