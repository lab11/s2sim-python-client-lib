import binascii

def hex_str_bytes(hex_str):
        return bytearray(hex_str.decode("hex"))

def int_bytes(integer):
	hex_str = hex(integer).replace('0x', '')
	if len(hex_str) % 8 != 0:
		hex_str = "0"*(8-len(hex_str)%8) + hex_str
	return hex_str_bytes(hex_str)

def print_bytearray(bytearray):
	print(binascii.hexlify(bytearray))

if __name__=="__main__":
	int_bytes(350)