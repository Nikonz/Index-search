#!/usr/bin/env python

import sys
import os
import func
import struct
from collections import defaultdict
from collections import OrderedDict

PATH = "./files/"

terms = defaultdict(list)

enc = func.Encoder()
denc = func.Encoder()
fenc = func.Encoder()
encMode = ""
prev = 0

def optimize(h, arr):
    global enc
    global denc
    global fenc

    res = []
    last = 0
    with open(func.PATH + "preIdx.data") as f:
        for val in arr:
            tmp = enc.unpackIdx(f, val)
            tmp[0] -= last
            res.extend(tmp)
            last += sum(tmp)
    with open(func.PATH + "dict.data", 'ab') as f:
        global prev
        prev = h
        if fenc.wasWroteTerm() * func.PAGE_SIZE <= denc.wasWroteTerm() * func.TERM_SIZE:
            with open(func.PATH + "fastDict.data", 'ab') as fdct:
                fenc.packTerm(fdct, h, denc.wasWroteTerm())
        denc.packTerm(f, h, enc.wasWrote())

    with open(func.PATH + "idx.data", 'ab') as f:
        enc.packIdx(f, res)


def main():
    with open(func.PATH + "preDict.data", 'rb') as f:
        f.seek(-1, 2)
        encMode = ('simple9' if struct.unpack('B', f.read(1))[0] == 1 else 'varbyte') 
        e = func.Encoder(encMode)
        idx = 0
        size = os.path.getsize(func.PATH + "preDict.data") / func.TERM_SIZE
        while idx < size:
            h, pos = e.unpackTerm(f, idx)
            terms[h].append(pos)
            idx += 1

    global enc
    global denc
    global fenc
    enc.changeMode(encMode)
    fenc.changeMode(encMode)
    denc.changeMode(encMode)

    tmp = sorted(terms.items())
    for key, value in tmp:
        optimize(key, value)          
    with open(func.PATH + "fastDict.data", 'ab') as fdct:
        fdct.write(struct.pack('B', 1 if encMode == 'simple9' else 0))  
            

if __name__ == '__main__':
    main()
