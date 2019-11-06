## gentrack.py - Generates a track file for LEGO Stunt Rally. By Yellowberry, MIT license.

import sys, struct, array, random

import lsrutil as s # other python file

### Variables and constants

lego_header = b'LEGO MOTO\0\0\0' # LEGO MOTO plus 3 null bytes, contents aren't checked

trk_size = 1 # 0 - Multi, 1 - Single
trk_theme = 3 # 0 - Jungle, 1 - Ice, 2 - Desert, 3 - City
trk_time = 1 # 0 - Day, 1 - Night

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

### Main logic

scr = bytearray(b'')

addBytes(scr, lego_header) # Init scratch file with header
addBytes(scr, struct.pack("<i", 5)) # Unsure, causes crash if changed, the "crash int"
addBytes(scr, struct.pack("<i", 65576)) # Filesize (65576), game will only recognize files with this specific file size
addBytes(scr, struct.pack("<i", trk_size)) # Track Size
addBytes(scr, struct.pack("<i", trk_theme)) # Track Scenery Theme
addBytes(scr, struct.pack("<i", trk_time)) # Track Time of Day

## Build track

loop = 8*(trk_size+1) # 8 - multi, 16 - single

addPiece(scr, 0, 0) # make the start line 
for h in range(loop-1):
	addPiece(scr, 30) # build track
addTrackPad(scr, trk_size)
for h in range(loop-1):
	for i in range(loop):
		addPiece(scr, 30) # build track
	addTrackPad(scr, trk_size)

scr = scr.ljust(65572, b'\0') # Pad file with 0x00 until 64kb is reached

addBytes(scr, struct.pack("<i",1))

## Write to file

print(scr)
trkfile = bytes(scr)

with open("python.trk", "wb") as bf:
    bw = bf.write(trkfile)
    print("Wrote %d bytes." % bw)