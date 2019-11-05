## gentrack.py - Generates a track file for LEGO Stunt Rally. By Yellowberry, MIT license.

import sys, struct, array, random

import lsrutil as s # other python file

### Variables and constants

lego_header = b'LEGO MOTO\x00\x00' # LEGO MOTO plus 3 null bytes, contents aren't checked, using last one to store custom info
trk_cst_version = 1 # The version number of the track file, 0 if vanilla, 1 if custom (comments, etc)

trk_size = 1 # 0 - Multi, 1 - Single
trk_theme = 3 # 0 - Jungle, 1 - Ice, 2 - Desert, 3 - City
trk_time = 1 # 0 - Day, 1 - Night
trk_comment = "Hey, this is a test of a track comment. Pretty nifty."

#with open('gentrack.py', "rb") as file:
#	gay = file.read()
#	trk_comment = gay.decode("utf-8") 

### Function defintions

## Lookup tables

def calcHeight(height): # 0 - 3
	h = b'' # Little endian float (DCBA)
	if height == 0:
		h = struct.pack("<f",-1) # -1 (BF 80 00 00)
	else:
		if   height == 1: h = struct.pack("<f", 8) #  8 (41 00 00 00)
		elif height == 2: h = struct.pack("<f",16) # 16 (41 80 00 00)
		elif height == 3: h = struct.pack("<f",24) # 24 (41 C0 00 00)
	return h

def calcTheme(theme = -1): # 0 - 3
	t = b''
	if theme == -1:
		return calcTheme(trk_theme) # cheap trick to pass the track theme instead
	else:
		if   theme == 0: t = b'\x3B' # Jungle
		elif theme == 1: t = b'\x3F' # Ice
		elif theme == 2: t = b'\x47' # Desert
		elif theme == 3: t = b'\x43' # City
	return t

def calcPiece(id, theme):
	p = b''
	if id == -1: 
		return b'\xFF\xFF\xFF\xFF' # Empty piece
	else:
		if theme == -1: theme = trk_theme # Theme missing, use map theme

		if   theme == 0: p += s.pi_jung[id] # Jungle
		elif theme == 1: p += s.pi_ice[id]  # Ice
		elif theme == 2: p += s.pi_dsrt[id] # Desert
		elif theme == 3: p += s.pi_city[id] # City
		p += calcTheme(theme) # Tack on theme type
		p += bytes(2) # empty bois
	return p

## Byte Manipulation

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
	struct.pack("<i", rotation) # Rotation
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
addBytes(scr, s.ib(trk_cst_version)) # Version byte
addArray(scr, [b'\x05', bytes(3)]) # Unsure, causes crash if changed
addBytes(scr, b'\x28\x00\x01\x00') # Filesize (65576), game will only recognize files with this specific file size
addArray(scr, [s.ib(trk_size),  bytes(3)]) # Track Size
addArray(scr, [s.ib(trk_theme), bytes(3)]) # Track Scenery Theme
addArray(scr, [s.ib(trk_time),  bytes(3)]) # Track Time of Day

## Build track

addPiece(scr, 0, 0) # make the start line
for h in range(15):
	addPiece(scr, 30, random.randint(0,3)) # build track
addTrackPad(scr, trk_size)
for h in range(15):
	for i in range(16):
		addPiece(scr, 30, random.randint(0,3)) # build track
	addTrackPad(scr, trk_size)

addComment(scr, trk_comment)

scr = scr.ljust(65576, b'\x00') # Pad file with 0x00 until 64kb is reached

## Write to file

print(scr)
trkfile = bytes(scr)

with open("_python.trk", "wb") as bf:
    bw = bf.write(trkfile)
    print("Wrote %d bytes." % bw)