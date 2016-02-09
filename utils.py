#!/usr/bin/env python3
# -*- encoding: utf8 -*-
###########################
## Utils for Python-MT
##
##
#

from io import BytesIO

def posFromInt(pos, blocksize):
    posx, posy = 0, 0

    posx = pos%blocksize
    pos -= posx
    pos  = int(pos/blocksize)

    posy = pos%blocksize
    pos -= posy
    pos  = int(pos/blocksize)

    return Pos({'x': posx, 'y': posy, 'z': pos})

def intFromPos(pos, blocksize):
    posint =  0
    posint += pos.x
    posint += pos.y * blocksize
    posint += pos.z * blocksize * blocksize
    return posint

def int64(u):
    while u >= 2**63:
        u -= 2**64
    while u <= -2**63:
        u += 2**64
    return u

def getMapBlockPos(pos):
    return pos.z * 4096 * 4096 + pos.y * 4096 + pos.x

def getIntegerAsBlock(i):
    x = unsignedToSigned(i % 4096, 2048)
    i = int((i - x) / 4096)
    y = unsignedToSigned(i % 4096, 2048)
    i = int((i - y) / 4096)
    z = unsignedToSigned(i % 4096, 2048)
    i = int((i - z) / 4096)
    return Pos({"x": x, "y": y, "z": z})

def unsignedToSigned(i, max_positive):
    if i < max_positive:
        return i
    else:
        return i - 2*max_positive

class Pos:
    def __init__(self, posdict = {"x": 0, "y": 0, "z": 0}):
        self.dict = posdict
        self.x = posdict.get("x") or 0
        self.y = posdict.get("y") or 0
        self.z = posdict.get("z") or 0

    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __repr__(self):
	    return str(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def getAsInt(self, max_val = 16):
        return int64(self.z * max_val * max_val + self.y * max_val + self.x)

    def getAsTuple(self):
        return (self.x, self.y, self.z)

    def fromTuple(self, tup):
        if len(tup) < 3:
            return False

        self.x, self.y, self.z = tup[0], tup[1], tup[2]
        self.dict = {'x': self.x, 'y': self.y, 'z': self.z}
        return self

# Thanks to @gravgun/elementW for those
# Big-endian!!!
def readU8(strm):
    return (ord(strm.read(1)))

def readU16(strm):
	#return (ord(strm.read(1)) << 16) + (ord(strm.read(1)))
	return (ord(strm.read(1)) << 8) + (ord(strm.read(1)))

def readU32(strm):
	return (ord(strm.read(1)) << 24) + (ord(strm.read(1)) << 16) + (ord(strm.read(1)) << 8) + (ord(strm.read(1)))

# Works with eight-bit two's complement
def readS8(strm):
    u = readU8(strm)
    if u & pow(2,7): # Negative
        return -pow(2,7) + (u-pow(2,7))
    else:
        return u

def readS16(strm):
    u = readU16(strm)
    if u & pow(2,15): # Negative
        return -pow(2,15) + (u-pow(2,15))
    else:
        return u

def readS32(strm):
    u = readU32(strm)
    if u & pow(2,31): # Negative
        return -pow(2,31) + (u-pow(2,31))
    else:
        return u

def writeU8(strm, val):
    strm.write(bytes([val]))#bytes(chr(val), encoding = 'utf8'))

def writeU16(strm, val):
    vals = []
    for _ in range(2):
        k = val % 256
        vals.insert(0, int(k))
        val -= k
        val /= 256

    strm.write(bytes(vals))

def writeU32(strm, val):
    vals = []
    for _ in range(4):
        k = val % 256
        vals.insert(0, int(k))
        val -= k
        val /= 256

    strm.write(bytes(vals))