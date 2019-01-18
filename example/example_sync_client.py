#!/usr/bin/python3
# -*- coding: utf-8 -*-

from spamclib.spamc_sync_client import SyncSpamcClient

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

if __name__ == '__main__':
    sc = SyncSpamcClient()
    # ping cannot support SpamAssassinForWindows
    sc.command_ping()
    sc.command_skip()
    res = sc.command_check(GTUBE.encode('utf-8'))
    print(res)
    print('Status code : %d' % res.status_code)
    print('Status message : %s' % res.status_message.decode('utf-8'))
    print('Header item Spam : %s' % res.get_header(b'Spam').decode('utf-8'))
    print('Response body : %s' % res.body.decode('utf-8'))
    sc.command_headers(GTUBE.encode('utf-8'))
    sc.command_process(GTUBE.encode('utf-8'))
    sc.command_report(GTUBE.encode('utf-8'))
    sc.command_report_ifspam(GTUBE.encode('utf-8'))
    sc.command_symbols(GTUBE.encode('utf-8'))
    pass
