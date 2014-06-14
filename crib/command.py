#!/usr/bin/env python

from subprocess import call
import os, argparse, getpass
import crib
from sys import platform

def main():
	# ----------------------------------------
	# Initialize parser

	parser = argparse.ArgumentParser(description = 'crib is a minimal command line encryption tool')
	parser.add_argument('-e', '--encrypt',
					help = 'Encrypts a file')
	parser.add_argument('-d', '--decrypt',
					help = 'Decrypts a file')
	parser.add_argument('-s', '--show',
					help = 'Opens a file for editing and / or viewing')

	args = vars(parser.parse_args())

	# -----------------------------------------
	# Action handling

	if args['encrypt']:
		# If encryption is to be done
		password = ""
		while True:
			print "Enter password for encryption"
			first_password = getpass.getpass()
			print "Confirm password"
			second_password = getpass.getpass()

			if first_password != second_password:
				print "Passwords dont match. Try again"
			else:
				print "Passwords match. Encrypting . . ."
				password = second_password
				break

		if crib.encrypt(crib.keygen(password), args['encrypt']) == 1:
			os.remove(args['encrypt'])
			print "Encryption done"
		else:
			print "Something wicked happened"

	elif args['decrypt']:
		# If decryption is to be done
		password = getpass.getpass()
		if crib.decrypt(crib.keygen(password), args['decrypt']) == 1:
			os.remove(args['decrypt'])
			print "Decryption done"
		else:
			print "Something wicked happened"

	elif args['show']:
		# If reading or editing the file is needed
		# It performs temporary decryption
		password = getpass.getpass()
		if crib.decrypt(crib.keygen(password), args['show']) == 1:
			os.remove(args['show'])
			print "Decryption done"
		else:
			print "Something wicked happened"
		
		file_name = os.path.splitext(args['show'])[0]
		
		try:
			if platform == "linux" or platform == "linux2":
				# Linux based OS detected
				# call(("xdg-open", file_name))
				call(("xdg-open", file_name))
			elif platform == "win32":
				# Windows detected
				os.startfile(file_name)
			elif platform == "darwin":
				# Mac OS detected
				call(("open", file_name))
		except:
				print "Error in opening file"

		if crib.encrypt(crib.keygen(password), file_name) == 1:
			os.remove(file_name)
			print "Re-encrypted"