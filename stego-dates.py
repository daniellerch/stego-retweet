#!/usr/bin/python

import sys
import md5
import json
import math
import time
import datetime
import textwrap
import numpy as np


BYTES_PER_TWEET=2
BLOCK_SIZE = 2**(BYTES_PER_TWEET*8) - 1

def get_dates(max_date):
    time_max = datetime.datetime.strptime(max_date, "%Y-%m-%d")
    ts = int(time.mktime(time_max.timetuple()))
    n = 0
    dates = []
    while n<BLOCK_SIZE:
        dates.append(ts)
        ts -= 60
        n += 1
    return dates

def get_cover(dates):
    bits = []
    for d in dates:
        hx = md5.new(str(d)).hexdigest()
        b = int(hx, 16)%2
        bits.append(b)
    return np.array(bits)

def prepare_M(n_bits):
    M=[]
    l=len(bin(2**n_bits-1)[2:])
    #print "ME len:", 2**n_bits
    for i in range(1, 2**n_bits):
        string=bin(i)[2:].zfill(l)
        V=[]
        for c in string:
            V.append(int(c))
        M.append(V)
    M=np.array(M).T

    return M

def ME_hide_block(M, c, m):
    r=m-M.dot(c)
    r=r%2

    idx=0
    found=False
    for i in M.T:
        if np.array_equal(i, r):
            found=True
            break
        idx+=1

    # the block does not need to be modified
    if not found:
        return c

    s=np.array(c)
    if s[idx]==0: s[idx]=1
    else: s[idx]=0

    return s, idx

def ME_unhide_block(M, s):
    m=M.dot(s)
    m=m%2
    return m


def str_to_bits(s):
    while len(s) % BYTES_PER_TWEET != 0:
        s += " "

    x = [ord(c) for c in s]
    y = [(b >> i) & 1 for b in x for i in reversed(range(8)) ]
    return np.array(y)

def bits_to_str(bits):
    chars=''
    for i in range(0, len(bits), 8):
        c_bits = bits[i:i+8]
        c_bits_str = ''.join(map(str, c_bits))
        chars += chr(int(c_bits_str, 2))
    return chars


def main():

    if len(sys.argv) != 4:
        print "Usage: "
        print "   %s <YY-MM-DD> <hide> <text>" % (sys.argv[0])
        print "   %s <YY-MM-DD> <unhide> <tweet ids>" % (sys.argv[0])
        print 
        sys.exit(0)

    dates = get_dates(sys.argv[1])
    C = get_cover(dates)
    M=prepare_M(BYTES_PER_TWEET*8) 
    #print "M:", M.shape

    if sys.argv[2] == 'hide':

        message = sys.argv[3]
        #print message
        #print "cover shape:", C.shape

        to_retweet=[]
        for mm in textwrap.wrap(message, BYTES_PER_TWEET, drop_whitespace=False):
            m = str_to_bits(mm)

            ##print "original = ", m 

            S, i = ME_hide_block(M, C, m) 
            d = datetime.datetime.fromtimestamp(dates[i]).strftime('%Y%m%d%H%M')
            to_retweet.append(d)

            #m_recovered=ME_unhide_block(M, S) 
            #print "extracted =", m_recovered 

        print ','.join(to_retweet)

    elif sys.argv[2] == 'unhide':

        retweets = sys.argv[3].split(",")
        message=''
        for r in retweets:
            time_max = datetime.datetime.strptime(r, "%Y%m%d%H%M")
            ts = int(time.mktime(time_max.timetuple()))
            try:
                idx = dates.index(ts)
            except:
                print "Date not found"
            S = C.copy()
            S[idx]=not S[idx]
            m_recovered=ME_unhide_block(M, S) 
            #print "extracted =", m_recovered 
            message += bits_to_str(m_recovered)
        print "message:", message

if __name__ == "__main__":
    main()






