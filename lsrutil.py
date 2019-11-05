# lsrutil.py - Contains a few useful things for LSR stuff. By Yellowberry, MIT license.

## Piece indexes

pi_city = [b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3B', b'\x3C', b'\x3F', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4D', b'\x4E', b'\x4F', b'\x50', b'\x51', b'\x53', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x66', b'\x67', b'\x68', b'\x6C', b'\x6D', b'\x6E', b'\x6F', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7D', b'\x7E', b'\x7F', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90']
pi_dsrt = [b'\x1D', b'\x19', b'\x1A', b'\x1B', b'\x1C', b'\x1E', b'\x1F', b'\x20', b'\x21', b'\x23', b'\x24', b'\x27', b'\x28', b'\x29', b'\x2A', b'\x2B', b'\x2C', b'\x2D', b'\x2E', b'\x2F', b'\x30', b'\x31', b'\x32', b'\x33', b'\x34', b'\x35', b'\x36', b'\x37', b'\x38', b'\x39', b'\x3B', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47', b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4E', b'\x4F', b'\x50', b'\x54', b'\x55', b'\x56', b'\x57', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78']
pi_jung = [b'\x65', b'\x61', b'\x62', b'\x63', b'\x64', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6B', b'\x6C', b'\x6F', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7D', b'\x7E', b'\x7F', b'\x80', b'\x81', b'\x83', b'\x88', b'\x89', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x66', b'\x97', b'\x98', b'\x9C', b'\x9D', b'\x9E', b'\x9F', b'\xA0', b'\xA1', b'\xA2', b'\xA3', b'\xA4', b'\xA5', b'\xA6', b'\xA7', b'\xA8', b'\xA9', b'\xAA', b'\xAB', b'\xAC', b'\xAD', b'\xAE', b'\xAF', b'\xBA', b'\xBB', b'\xBC', b'\xBD', b'\xBE', b'\xBF', b'\xC0']
pi_ice  = [b'\x48', b'\x49', b'\x4A', b'\x4B', b'\x4C', b'\x4E', b'\x4F', b'\x50', b'\x51', b'\x53', b'\x54', b'\x57', b'\x58', b'\x59', b'\x5A', b'\x5B', b'\x5C', b'\x5D', b'\x5E', b'\x5F', b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67', b'\x68', b'\x69', b'\x6B', b'\x70', b'\x71', b'\x72', b'\x73', b'\x74', b'\x75', b'\x76', b'\x77', b'\x78', b'\x79', b'\x7A', b'\x7B', b'\x7C', b'\x7E', b'\x7F', b'\x80', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8A', b'\x8B', b'\x8C', b'\x8D', b'\x8E', b'\x8F', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\xA2', b'\xA3', b'\xA4', b'\xA5', b'\xA6', b'\xA7', b'\xA8']

## Clean names for values

t_theme = ["Jungle", "Desert", "Ice", "City"]
t_size = ["Multiplayer", "Singleplayer"]
t_time = ["Day", "Night"]

## Helper functions

def ib(int): # int -> byte
	return bytes([int])

def bi(byte): # byte -> int
	return byte[0]

def bAdd(a, b): # can only add to 255, errors otherwise
	return ib(bi(a) + bi(b))