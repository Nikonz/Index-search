#!/usr/bin/env python
#coding: utf-8 -*- 

import sys
import os
import func
import struct
from collections import defaultdict
from bisect import bisect_right
from sets import Set

urls = []
fterms = {}
lterms = []
encMode = ''

def compute(req):
    query = parse(req)
    #print query
    res = []     #[(Set(), False) for i in len(query)] 
    for tok in query:
        if tok in ['&', '|']:
            if res[-2][1] == res[-1][1]:
                if (tok == '&') != res[-1][1]:
                    res[-2][0].intersection_update(res[-1][0])
                else:
                    res[-2][0].update(res[-1][0])
            else:
                if (tok == '&') == res[-2][1]:
                    res[-1][0].difference_update(res[-2][0])
                    #print len(res[-1][0]) 
                    res[-2] = (res[-1][0], tok == '|')
                else:
                    res[-2][0].difference_update(res[-1][0])
                    res[-2] = (res[-2][0], tok == '|')
            res = res[: -1]
        elif tok == '!':
            res[-1] = (res[-1][0], not res[-1][1])
        else:
            res.append((getDocs(getIdxPos(tok)), False))
    #print res[0][0]
    print req
    resUrls = getUrls(sorted(res[0][0]))
    print len(resUrls)
    for u in resUrls:
        print u[:-1]

def parse(req):
    def prior(bc, op):
        return (bc << 2) | ((op == '!') << 1) | (op == '&')

    ans = []
    oper = []
    bc = 0
    v = ""  
    for i in req:
        if i == ' ':
            continue
        elif i in ['(', ')', '&', '|', '!']:
            if len(v) > 0:
                ans.append(v)
                v = ""
            if i in ['(', ')']:
                bc += (i == '(') * 2 - 1
            else:
                while len(oper) > 0 and prior(bc, i) <= oper[-1][1]:
                    #print (i, prior(bc, i)), oper[-1]
                    ans.append(oper[-1][0])
                    oper = oper[: -1]
                #print i
                oper.append((i, prior(bc, i)))
                #print oper
        else:
            v += i
    if len(v) > 0:
        ans.append(v)
    for i in xrange(len(oper) - 1, -1, -1):
        ans.append(oper[i][0])

    return ans

def getIdxPos(token):
    token = unicode(token, 'utf-8')
    hTok = func.myHash(token.lower())
    enc = func.Encoder(encMode)
    #print 'ddd'
    with open(func.PATH + "dict.data", 'rb') as dct:
        num = bisect_right(lterms, hTok)
        if num == 0:
            return None
        l = fterms[lterms[num - 1]]
        r = fterms[lterms[num]]
        #print l, r
        while l + 1 < r:
            m = (l + r) / 2
            #print enc.unpackTerm(dct, m)[0]
            #print hTok, enc.unpackTerm(dct, m)[0]
            if hTok < enc.unpackTerm(dct, m)[0]:
                r = m
            else:
                l = m
        h, val = enc.unpackTerm(dct, l)
        #print h, hTok, " OK"
        if hTok == h:
            #print "Posss = ", val
            return val
    return None

def getDocs(pos):
    if pos is None:
        return Set()
    #ans = []
    #print "Pos = ", pos
    ans = Set()
    last = 0
    enc = func.Encoder(encMode)
    with open(func.PATH + "idx.data", 'rb') as idx:
        ids = enc.unpackIdx(idx, pos)
        #print "ids = ", pos, ids
        for x in ids:
            x += last
            #ans.append(x)
            ans.add(x)
            last = x
    #print "Ans = ", ans
    return ans

def getUrls(idx):
    global urls
    ans = []
    #print idx
    for i in idx:
        ans.append(urls[i])
    return ans

def main():
    global encMode
    with open(func.PATH + "urls.list", 'r') as f:
        for line in f:
            urls.append(line)
    with open(func.PATH + "fastDict.data", 'rb') as fdct:
        fdct.seek(-1, 2)
        encMode = ('simple9' if struct.unpack('B', fdct.read(1))[0] == 1 else 'varbyte') 
        size = os.path.getsize(func.PATH + "fastDict.data") / func.TERM_SIZE
        enc = func.Encoder(encMode)
        #print encMode
        i = 0
        while i < size:
            h, pos = enc.unpackTerm(fdct, i)
            #print h, pos
            lterms.append(h)
            fterms[h] = pos
            i += 1
    lterms.append(1 << 63)
    fterms[1 << 63] = os.path.getsize(func.PATH + "dict.data") / func.TERM_SIZE
    
    #print lterms
    #print fterms
    while True:
        try:
            req = raw_input()
            if req == "":
                break
            compute(req)
        except (EOFError):
            break


if __name__ == '__main__':
    main()
