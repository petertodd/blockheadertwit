#!/usr/bin/python
#
# (c) 2013 Peter Todd
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from binascii import *
import jsonrpc
import struct
import sys
import twitter

proxy_url = 'http://user:pass@localhost:8332'
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

bitcoin_header_format = struct.Struct("<i 32s 32s I 4s I")
def serialize_block_header(block):
    """Serialize a block header from the RPC interface"""
    return bitcoin_header_format.pack(
        block['version'],
        unhexlify(block['previousblockhash'])[::-1],
        unhexlify(block['merkleroot'])[::-1],
        block['time'],
        unhexlify(block['bits'])[::-1],
        block['nonce'])

proxy = jsonrpc.ServiceProxy(proxy_url)


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

def tweet_block(block_hash, proxy, api):
    block = proxy.getblock(block_hash)
    height = block['height']
    block = serialize_block_header(block)

    txt_block = '#bitcoin #btcblkhdr %d: %s' % (height, b2a_base64(block))

    return api.PostUpdate(txt_block)

print tweet_block(sys.argv[1], proxy, api)
