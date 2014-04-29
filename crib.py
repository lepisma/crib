#!/usr/bin/python

from subprocess import call
from Crypto.Cipher import AES
import os, random, struct, hashlib, argparse, getpass

def pass_to_key(password):
	return hashlib.sha256(password).digest()

def encrypt(key, file_name, chunksize = 64 * 1024):
	# Encrypts the file
	output = file_name + '.enc'
	
	IV = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	file_size = os.path.getsize(file_name)

	with open(file_name, 'rb') as infile:
		with open(output, 'wb') as outfile:
			outfile.write(struct.pack('<Q', file_size))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - len(chunk) % 16)

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, file_name, chunksize = 24 * 1024):
	# Decrypts the file
	output = os.path.splitext(file_name)[0]

	with open(file_name, 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		IV = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(output, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(origsize)


parser = argparse.ArgumentParser(description = 'crib is a minimal command line encryption tool')
parser.add_argument('-e', '--encrypt',
				help = 'Encrypts a file')
parser.add_argument('-d', '--decrypt',
				help = 'Decrypts a file')
parser.add_argument('-s', '--show',
				help = 'Opens a file for editing and / or viewing')

args = vars(parser.parse_args())

if args['encrypt']:
	password = getpass.getpass()
	encrypt(pass_to_key(password), args['encrypt'])
	os.remove(args['encrypt'])

elif args['decrypt']:
	password = getpass.getpass()
	decrypt(pass_to_key(password), args['decrypt'])
	os.remove(args['decrypt'])

elif args['show']:
	password = getpass.getpass()
	decrypt(pass_to_key(password), args['show'])
	os.remove(args['show'])
	
	file_name = os.path.splitext(args['show'])[0]
	
	call(("nano", file_name))

	encrypt(pass_to_key(password), file_name)
	os.remove(file_name)