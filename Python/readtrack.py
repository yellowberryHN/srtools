## readtrack.py - Reads a LEGO Stunt Rally track file. By Yellowberry, MIT license.

import os, sys, struct, array, random

import lsrutil as s # other python file

### Functions

def getTheme(theme):
	t = -1
	if   theme == b'\x3B': t = 0 # Jungle
	elif theme == b'\x3F': t = 1 # Ice
	elif theme == b'\x47': t = 2 # Desert
	elif theme == b'\x43': t = 3 # City
	return t

def getNid(id, theme):
	ret = 0
	if   theme == 0: tb = s.pi_jung # Jungle
	elif theme == 1: tb = s.pi_ice  # Ice
	elif theme == 2: tb = s.pi_dsrt # Desert
	elif theme == 3: tb = s.pi_city # City
	for h in tb:
		if h == id:
			break
		ret += 1
	return ret
 
def parsePiece(data):
	height = struct.unpack("<f", data[0])[0] # Unpack LE float
	if   height == -1: height = 0
	elif height ==  8: height = 1
	elif height == 16: height = 2
	elif height == 24: height = 3

	piece = data[1]
	theme = getTheme(piece[1:2])
	id = hex(piece[:1][0])
	nid = getNid(s.ib(int(id, 16)), theme)

	rotation = struct.unpack("<i", data[2])[0] # Unpack LE int

	#print(height, theme, id, nid)
	return [nid, id, theme, rotation, height]

def prettyPiece(x,y):
	info = parsePiece(trk_pieces[y][x])
	print("### Piece information for", "x" + str(x) + ",y" + str(y), "###")
	print("nID:", info[0])
	print("ID:", info[1])
	print("Theme:", s.t_theme[info[2]])
	print("Rotation:", info[3])
	print("Height:", info[4])

### Main logic

## Checking arguments
get_x = 0
get_y = 0
try:
	get_x = int(sys.argv[2])
	get_y = int(sys.argv[3])
except:
	pass # we take what we can get

## Opening file and collecting data

trk_name = os.path.basename(os.path.normpath(sys.argv[1]))
with open(sys.argv[1], "rb") as file:

	realsize = os.path.getsize(sys.argv[1]) # get actual filesize

	lego_header = file.read(12) # 'LEGO MOTO\0\0\0'
	crashint = struct.unpack("<i", file.read(4))[0] # Always 5
	trk_fsize = struct.unpack("<i", file.read(4))[0]
	if trk_fsize != 65576: raise Exception("Binary filesize reports non 64KB file!")
	elif realsize != trk_fsize: raise Exception("Incorrect filesize, corrupted track!")
	trk_size = struct.unpack("<i", file.read(4))[0] # 0 - 1
	trk_theme = struct.unpack("<i", file.read(4))[0] # 0 - 3
	trk_time = struct.unpack("<i", file.read(4))[0] # 0 - 1

	iters = 8*(trk_size+1)
	skip = (56-(trk_size*8))*16
	trk_pieces = []
	for x in range(iters):
		tmp = []
		for y in range(iters):
			piece = []
			file.read(4) # discard null bytes
			for z in range(3):
				piece.append(file.read(4))
			tmp.append(piece)
		file.read(skip)
		trk_pieces.append(tmp)	

## Printing info

#print(iters, skip)
#print(trk_pieces)
print("## Track information for", trk_name, "##")
print("Fizesize:", trk_fsize)
print("Track Type:", s.t_size[trk_size])
print("Track Theme:", s.t_theme[trk_theme])
print("Time of Day:", s.t_time[trk_time])
print("---")
prettyPiece(get_x,get_y)