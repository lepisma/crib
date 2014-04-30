
from Crypto.Cipher import AES
import random, struct, hashlib, os

def keygen(password):
	return hashlib.sha256(password).digest()

def encrypt(key, file_name, chunksize = 64 * 1024):
	# Encrypts the file
	output = file_name + '.crib'
	
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