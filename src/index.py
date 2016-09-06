#!/usr/bin/env python
#  #coding: utf-8

import sys
import re
from docreader import DocumentStreamReader
from sets import Set
from collections import defaultdict
import codecs
import struct

import func

terms = defaultdict(list)
enc  = func.Encoder()
denc = func.Encoder()
encMode = ""
curCnt = 0
curIdx = 0

def parse(text, docId):
    global terms
    global curCnt
    words = re.findall(r'\w+', text, re.U)

    elems = Set();
    for w in words:
        elems.add(func.myHash(w.lower()))
    curCnt += len(elems)
    for el in elems:
        terms[el].append(docId)        
    if curCnt > func.CNT_MAX:
        flush()
        curCnt = 0

def flush():
    global terms
    global denc
    global enc 
    with open(func.PATH + "preIdx.data", 'ab') as f, open(func.PATH + "preDict.data", 'ab') as dct: 
        for key, value in terms.items():
            denc.packTerm(dct, key, enc.wasWrote())
            tmp = []
            for i in xrange(len(value)):
                tmp.append(value[i] if i == 0 else value[i] - value[i - 1]);
            enc.packIdx(f, tmp)
        terms = defaultdict(list)

def flushUrls():
    global urls
    if len(urls) == 0:
        return
    with open(func.PATH + str(curUrl) + ".urls", "w") as f:
        for url in urls:
            f.write(url + "\n")
    urls = []


def main():
    encMode = sys.argv[1]
    enc.changeMode(encMode)
    denc.changeMode(encMode)    
    with open(func.PATH + "urls.list", "a") as urls:
        docId = 0
        for path in sys.argv[2:]:
            for doc in DocumentStreamReader(path):
                urls.write(doc.url + "\n")
                parse(doc.text, docId)
                docId += 1
    flush()
    with open(func.PATH + "preDict.data", 'ab') as dct:
        dct.write(struct.pack('B', 1 if encMode == 'simple9' else 0))

if __name__ == '__main__':
    main()
