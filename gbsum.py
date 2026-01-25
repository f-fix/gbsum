#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, binascii, locale

EXPECTED_LOGO_CHECKSUM = 0x46195417

ASCII_ALPHA_4 = ' .\':'
BLOCK_ALPHA_4 = u' ▄▀█'
BRAILLE_ALPHA_4 = u'\u2800\u28E4\u281B\u28FF'
BRAILLE_ALPHA_256 = u''.join(unichr(0x2800 + i) for i in xrange(256))

def vlogo4(alpha4, data, charset):
    def vlxpnd(u8):
        return u''.join(alpha4[{0x00: 0, 0x08: 1, 0x80: 2, 0x88: 3}[((u8 << i) & 0x88)]] for i in xrange(4))
    return (u'\n'.join(u''.join(vlxpnd(ord(data[i])) for i in xrange(len(data)) if i & 1 == e) for e in (0, 1))
            ).encode(charset)

XPM256 = {
    sum((0x8000 if i & 0x80 else 0,
         0x4000 if i & 0x40 else 0,
         0x0800 if i & 0x20 else 0,
         0x0400 if i & 0x10 else 0,
         0x0080 if i & 0x08 else 0,
         0x0040 if i & 0x04 else 0,
         0x0008 if i & 0x02 else 0,
         0x0004 if i & 0x01 else 0)): i
    for i in xrange(256)
    }

def vlogo256(alpha256, data, charset):
    def vlxpnd(u16):
        return u''.join(alpha256[XPM256[((u16 << (2 * i)) & 0xCCCC)]] for i in xrange(2))
    return u''.join(vlxpnd((ord(data[i]) << 8) | ord(data[i + 1])) for i in xrange(len(data)) if i & 1 == 0).encode(charset)

def goodcs(charset):
    try:
        charset = charset.lower()
        assert u'HELLO'.encode(charset, 'replace').decode(charset) == u'HELLO'
        return charset
    except:
        pass
    return None

def vlogo(data):
    charset = goodcs(os.environ.get('CHARSET')) or goodcs(os.environ.get('DEFAULT_CHARSET')) or goodcs(locale.getpreferredencoding()) or 'us-ascii'
    if charset != 'utf-8':
        alpha4 = ASCII_ALPHA_4
        if BLOCK_ALPHA_4.encode(charset, 'replace').decode(charset) == BLOCK_ALPHA_4:
            alpha4 = BLOCK_ALPHA_4
        return vlogo4(alpha4, data[:24], charset) + '\n' + vlogo4(alpha4, data[24:], charset)
    alpha256 = [BRAILLE_ALPHA_256[sum((0x01 if i & 0x80 else 0,
                                       0x08 if i & 0x40 else 0,
                                       0x02 if i & 0x20 else 0,
                                       0x10 if i & 0x10 else 0,
                                       0x04 if i & 0x08 else 0,
                                       0x20 if i & 0x04 else 0,
                                       0x40 if i & 0x02 else 0,
                                       0x80 if i & 0x01 else 0))] for i in xrange(256)]
    return vlogo256(alpha256, data[:24], charset) + '\n' + vlogo256(alpha256, data[24:][:24], charset)

def main(progname, infile, outfile):
    verbose = True
    if infile == '-c':
        infile = outfile
        outfile = None
        verbose = False
    elif infile == '-v':
        infile = outfile
        outfile = None
    cart = file(infile, 'rb').read()
    ocart = cart
    logo_checksum = (0x100000000 + binascii.crc32(cart[0x104:][:48])) & 0xFFFFFFFF
    assert logo_checksum == EXPECTED_LOGO_CHECKSUM, ('%s: logo checksum mismatch: computed %08X vs. expected %08X' % (
        infile,
        logo_checksum,
        EXPECTED_LOGO_CHECKSUM)) + '\n' + vlogo(cart[0x104:][:48])
    header_checksum = 0
    for i in xrange(0x0134, 0x014D):
        header_checksum = (0x200 + (header_checksum - ord(cart[i]) - 1)) & 0xFF
    cart = cart[:0x014D] + chr(header_checksum) + cart[0x014E:]
    global_cksum = 0
    cart = cart[:0x014E] + chr(0) + chr(0) + cart[0x0150:]
    for i in xrange(len(cart)):
        global_cksum = (global_cksum + ord(cart[i])) & 0xFFFF
    cart = cart[:0x014E] + chr((global_cksum & 0xFF00) >> 8) + chr(global_cksum & 0xFF) + cart[0x0150:]
    if verbose:
        print("%s: recorded checksum %02X:%04X" % (infile, ord(ocart[0x14D]), (ord(ocart[0x14E]) << 8) | ord(ocart[0x14F])))
        print("%s: computed checksum %02X:%04X" % (infile, header_checksum, global_cksum))
        print(vlogo(cart[0x104:][:48]))
    if outfile is None:
        assert cart == ocart, '%s: checksum mismatch: computed %02X:%04X vs. recorded %02X:%04X' % (
            infile,
            header_checksum,
            global_cksum,
            ord(ocart[0x14D]),
            (ord(ocart[0x14E]) << 8) | ord(ocart[0x14F]))
        assert cart == ocart, 'INTERNAL ERROR IN ' + progname
    else:
        outfh = file(outfile, 'wb')
        outfh.write(cart)
        outfh.close()

if __name__ == '__main__':
    main(*sys.argv) # usage: python gbsum.py { -c -OR- -v } FILE.GB  -OR-  python gbsum.py FILE.GB OUTFILE.GB 
