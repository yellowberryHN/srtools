## gentrack.py - Generates a track file for LEGO Stunt Rally. By Yellowberry, MIT license.

import sys, struct, array, random

### Variables and constants

lego_header = b'LEGO MOTO\x00\x00' # LEGO MOTO plus 3 null bytes, contents aren't checked, using last one to store custom info
trk_cst_version = 1 # The version number of the track file, 0 if vanilla, 1 if custom (comments, etc)

trk_size = 1 # 0 - Multi, 1 - Single
trk_theme = 0 # 0 - Jungle, 1 - Ice, 2 - Desert, 3 - City
trk_time = 1 # 0 - Day, 1 - Night
#trk_comment = "Hey, this is a test of a track comment. Pretty nifty."

with open('gentrack.py', "rb") as file:
	gay = file.read()
	trk_comment = gay.decode("utf-8") 

### Function defintions

## Lookup tables

## Piece indexes
pi_city = [b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3B', b'\x3C', b'\x3F', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4D', b'\x4E', b'\x4F', b'\x50', b'\x51', b'\x53', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x66', b'\x67', b'\x68', b'\x6C', b'\x6D', b'\x6E', b'\x6F', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7D', b'\x7E', b'\x7F', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90']
pi_dsrt = [b'\x1D', b'\x19', b'\x1A', b'\x1B', b'\x1C', b'\x1E', b'\x1F', b'\x20', b'\x21', b'\x23', b'\x24', b'\x27', b'\x28', b'\x29', b'\x2A', b'\x2B', b'\x2C', b'\x2D', b'\x2E', b'\x2F', b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3B', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4E', b'\x4F', b'\x50', b'\x54', b'\x55', b'\x56', b'\x57', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78']
pi_jung = [b'\x65', b'\x61', b'\x62', b'\x63', b'\x64', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6B', b'\x6C', b'\x6F', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7D', b'\x7E', b'\x7F', b'\x80', b'\x81', b'\x83', b'\x88', b'\x89', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x66', b'\x97', b'\x98', b'\x9C', b'\x9D', b'\x9E', b'\x9F', b'\xA0', b'\xA1', b'\xA2', b'\xA3', b'\xA4', b'\xA5', b'\xA6', b'\xA7', b'\xA8', b'\xA9', b'\xAA', b'\xAB', b'\xAC', b'\xAD', b'\xAE', b'\xAF', b'\xBA', b'\xBB', b'\xBC', b'\xBD', b'\xBE', b'\xBF', b'\xC0']
pi_ice  = [b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4E', b'\x4F', b'\x50', b'\x51', b'\x53', b'\x54', b'\x57', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6B', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7E', b'\x7F', b'\x80', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\xA2', b'\xA3', b'\xA4', b'\xA5', b'\xA6', b'\xA7', b'\xA8']

def calcHeight(height): # 0 - 3
	h = b'\x00\x00' # Little endian float (DCBA)
	if height == 0:
		h += b'\x80\xBF' # -1 (BF 80 00 00)
	else:
		if   height == 1: h += b'\x00' # 8 (41 00 00 00)
		elif height == 2: h += b'\x80' # 16 (41 80 00 00)
		elif height == 3: h += b'\xC0' # 24 (41 C0 00 00)
		h += b'\x41'
	return h

def calcTheme(theme = -1): # 0 - 3
	t = b''
	if theme == -1:
		return calcTheme(trk_theme) # cheap trick to pass the track theme instead
	else:
		if   theme == 0: t += b'\x3B' # Jungle
		elif theme == 1: t += b'\x3F' # Ice
		elif theme == 2: t += b'\x47' # Desert
		elif theme == 3: t += b'\x43' # City
	return t

def calcPiece(id, theme):
	p = b''
	if id == -1: 
		return b'\xFF\xFF\xFF\xFF' # Empty piece
	else:
		if theme == -1: theme = trk_theme # Theme missing, use map theme

		if   theme == 0: p += pi_jung[id] # Jungle
		elif theme == 1: p += pi_ice[id]  # Ice
		elif theme == 2: p += pi_dsrt[id] # Desert
		elif theme == 3: p += pi_city[id] # City
		p += calcTheme(theme) # Tack on theme type
		p += bytes(2) # empty bois
	return p

## Byte Manipulation

def ib(int): # int -> byte
	return bytes([int])

def bi(byte): # byte -> int
	return byte[0]

def bAdd(a, b): # can only add to 255, errors otherwise
	return ib(bi(a) + bi(b))

def addNull(scr, amount): # adds null bytes, use bytes(x) instead.
	for x in range(amount):
		scr.append(0)

def addBytes(scr, data): # adds arbitrary bytes to scratch
	scr += data

def addArray(scr, array): # adds array of bytes to scratch
	addBytes(scr, b''.join(array))

def addPiece(scr, pieceId = -1, rotation = 0, height = 0, pieceTheme = -1):
	track = [
	bytes(4), # Null bytes, Unknown
	calcHeight(height), # Height, managed by calcHeight()
	calcPiece(pieceId, pieceTheme), # Piece ID and Theme
	ib(rotation), bytes(3) # Rotation
	]
	#print(track)
	addArray(scr, track)

def addTrackPad(scr, size):
	amt = 56-(size*8) # 48 for single, 56 for multi
	for p in range(amt):
		addArray(scr, [bytes(8), b'\xFF\xFF\xFF\xFF', bytes(4)])

def addComment(scr, comment):
	c = b''.join([bytes(10), b'CMNT\xFE\xFF'])
	c += bytes(comment, 'ascii')
	c += b'\xFF\xFE' # indicates the comment is over.
	addBytes(scr, c)


### Main logic

scr = bytearray(b'')

addBytes(scr, lego_header) # Init scratch file with header
addBytes(scr, ib(trk_cst_version)) # Version byte
addArray(scr, [b'\x05', bytes(3)]) # Unsure, causes crash if changed
addBytes(scr, b'\x28\x00\x01\x00') # Filesize (65576), game will only recognize files with this specific file size
addArray(scr, [ib(trk_size),  bytes(3)]) # Track Size
addArray(scr, [ib(trk_theme), bytes(3)]) # Track Scenery Theme
addArray(scr, [ib(trk_time),  bytes(3)]) # Track Time of Day

## Build track

addPiece(scr, 0, 0) # make the start line
for h in range(15):
	addPiece(scr, 30, random.randint(0,3), random.randint(0,3)) # build track
addTrackPad(scr, trk_size)
for h in range(15):
	for i in range(16):
		addPiece(scr, 30, random.randint(0,3), random.randint(0,3)) # build track
	addTrackPad(scr, trk_size)

addComment(scr, trk_comment)

scr = scr.ljust(65576, b'\x00') # Pad file with 0x00 until 64kb is reached

## Write to file

print(scr)
trkfile = bytes(scr)

with open("_python.trk", "wb") as bf:
    bw = bf.write(trkfile)
    print("Wrote %d bytes." % bw)