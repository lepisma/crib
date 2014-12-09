#!/usr/bin/env python

from subprocess import call
import os, argparse, getpass
import crib
from sys import platform

def main():
    # ----------------------------------------
    # Initialize parser

    parser = argparse.ArgumentParser(description = "crib is a minimal command line encryption tool")
    parser.add_argument("file",
                        help = "the file to be acted on")

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument("-e", "--encrypt",
                              help = "encrypts the file",
                              action = "store_true")
    action_group.add_argument("-d", "--decrypt",
                              help = "decrypts the file",
                              action = "store_true")
    action_group.add_argument("-s", "--show",
                        help = "temporarily opens the file for editing and / or viewing",
                        action = "store_true")

    args = parser.parse_args()

    # -----------------------------------------
    # Action handling

    if args.encrypt:
        # If encryption is to be done
        password = ""
        while True:
            print("Enter password for encryption")
            first_password = getpass.getpass()
            print("Confirm password")
            second_password = getpass.getpass()

            if first_password != second_password:
                print("Passwords dont match. Try again")
                print("")
            else:
                print("Passwords match. Encrypting . . .")
                password = second_password
                break

        if crib.encrypt(crib.keygen(password), args.file) == 1:
            os.remove(args.file)
            print("Encryption done")
        else:
            print("Something wicked happened")

    elif args.decrypt:
        # If decryption is to be done
        password = getpass.getpass()
        if crib.decrypt(crib.keygen(password), args.file) == 1:
            os.remove(args.file)
            print("Decryption done")
        else:
            print("Something wicked happened")

    elif args.show:
        # If reading or editing the file is needed
        # It performs temporary decryption
        password = getpass.getpass()
        if crib.decrypt(crib.keygen(password), args.file) == 1:
            os.remove(args.file)
            print("Decryption done")
        else:
            print("Something wicked happened")
		
        file_name = os.path.splitext(args.file)[0]
		
        try:
            if platform == "linux" or platform == "linux2":
                # Linux based OS detected
                call(("xdg-open", file_name))
            elif platform == "win32":
                # Windows detected
                os.startfile(file_name)
            elif platform == "darwin":
                # Mac OS detected
                call(("open", file_name))
        except:
            print("Error in opening file")

        print("Waiting on user . . .")
        print("Press return to re-encrypt the file.")
        raw_input()

        if crib.encrypt(crib.keygen(password), file_name) == 1:
            os.remove(file_name)
            print("Re-encrypted")
