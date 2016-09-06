import math
import struct

PATH = "./files/"
CNT_MAX = int(3e7)
BLK_MAX = int(4096 * 10)
PAGE_SIZE = 4096 # in block
TERM_SIZE = 12

detect = [1682220763423762]

def myHash(x):
    return hash(x) & ((1 << 62) - 1)

import os

class Encoder:
    mode = 'Simple9'    

    def __init__(self, mode='simple9'):
        self.changeMode(mode)
        self.wasTerm = 0

    def changeMode(self, mode):
        if mode == 'simple9':
            self.encoder = Simple9()
        elif mode == 'varbyte':
            self.encoder = VarByte()
        else:
            raise Exception('Encoder\'s mode is not supported')

    def packTerm(self, f, h, val):
        #print os.path.getsize(PATH + "preDict.data"), h, val
        self.wasTerm += 1
        #print h, val
        f.write(struct.pack('QI', h, val))

    def unpackTerm(self, f, pos):
        f.seek(pos * TERM_SIZE)
        z = f.read(TERM_SIZE)
        f.seek(pos * TERM_SIZE)
        return struct.unpack('QI', f.read(TERM_SIZE))

    def packIdx(self, f, vals):
        #print vals[:20]
        self.encoder.packIdx(f, vals)

    def unpackIdx(self, f, pos):
        #print 'unpack'
        x = self.encoder.unpackIdx(f, pos)
        return x

    def wasWrote(self):
        return self.encoder.wasWrote

    def wasWroteTerm(self):
        return self.wasTerm


class VarByte:
    def __init__(self):
        self.wasWrote = 0

    def packIdx(self, f, vals):
        self.writeVal(f, len(vals))
        #print len(vals)
        for v in vals:
            self.writeVal(f, v)

    def unpackIdx(self, f, pos):
        vals = []
        f.seek(pos)
        n = self.readVal(f)
        #print "N = ", n
        for i in xrange(n):
            vals.append(self.readVal(f))
        return vals

    def writeVal(self, f, v):
        #print v
        while v > 0:
            b = v & 127
            v >>= 7
            if v == 0:
                b |= 128
            #print 'B = ', b
            f.write(struct.pack('B', b))
            self.wasWrote += 1

    def readVal(self, f):
        val = 0
        #f.seek(0)
        cnt = 0
        while True:
            b = struct.unpack('B', f.read(1))[0]
            #print "B = ", b
            val |= (b & 127) << (7 * cnt)
            if b & 128 > 0:
                break
            cnt += 1
        #print val
        return val

class Simple9: 
    CELLS = [1, 2, 3, 4, 5, 7, 9, 14, 28]
    SIZE = 28
   
    def __init__(self):
        self.buf = []
        self.mCell = []
        self.wasWrote = 0

    def packIdx(self, f, vals):
        self.write(f, len(vals))
        self.writeVals(f, vals)
        self.flushAll(f)

    def unpackIdx(self, f, pos):
        vals, rd = self.readVals(f, pos, 1)
        #print vals[0], pos + rd
        tmp,  rd = self.readVals(f, pos + rd, vals[0] - (len(vals) - 1))
        vals.extend(tmp)
        return vals[1: vals[0] + 1]
    
    def writeVals(self, f, vals):
        for v in vals:
            self.write(f, v)          

    def readVals(self, f, pos, count):
        res = []
        wasRead = 0
        while len(res) < count:
            res.extend(self.read(f, pos + wasRead))
            wasRead += 4
        return (res, wasRead)

    def write(self, f, x):
        self.mCell.append(self.minCell(x))
        if len(self.buf) == self.SIZE:
            self.flush(f)
        self.buf.append(x)  

    def read(self, f, blockNum):
        f.seek(blockNum)
        data = (struct.unpack('I', f.read(4)))[0]
        mode = data & 15
        res = []
        offs = 4
        while offs + self.CELLS[mode] <= 32:
            res.append((data & (((1 << self.CELLS[mode]) << offs) - 1)) >> offs)
            offs += self.CELLS[mode]
        return res

    def flushAll(self, f):
        while len(self.buf) > 0:
            self.flush(f)

    def flush(self, f):
        mode = 0
        for i in xrange(len(self.CELLS)):
            idx = min(self.CELLS[-(i + 1)], len(self.buf))
            if max(self.mCell[:idx]) <= i:
                mode = i
                break
        offs = 4
        res = mode
        for x in self.buf[:self.CELLS[-(mode + 1)]]:
            res |= (x << offs)
            offs += self.CELLS[mode]
        f.write(struct.pack('I', res))
        self.wasWrote += 4
        self.buf   = self.buf[self.CELLS[-(mode + 1)]:]
        self.mCell = self.mCell[self.CELLS[-(mode + 1)]:]

    def minCell(self, x):
        n = self.lens(x)
        for i in xrange(9):
            if n <= self.CELLS[i]:
                return i    

    def lens(self, x):
        return math.ceil(math.log(x + 1, 2))
