#!/usr/local/bin/python
import argparse
import sys
import zipfile
import os
from termcolor import colored


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_WORD_LIST = os.path.join(SCRIPT_PATH, "wordlist", "zip.txt")

description = """
    zip cracker for hackercamp
    Example: python zip_cracker.py --file /home/user/file.zip --wordlist /home/user/wordlist.txt
"""

parser = argparse.ArgumentParser("zip cracker", description)
parser.add_argument("--wordlist", "-w", help="wordlist path, format:/home/user/wordlist.txt", default=DEFAULT_WORD_LIST)
parser.add_argument("--file", "-f", help="file path, format: /home/user/file.zip", required=True)
args = parser.parse_args()


def cracker():
    zip_file = zipfile.ZipFile(args.file)
    with open(args.wordlist, 'r') as f:
        for line in f.readlines():
            password = line.strip('\n')
            try:
                zip_file.extractall(pwd=password)
                print "Password has been found : {}".format(colored(password, "green"))
                exit()
            except zipfile.BadZipfile:
                print "Bad Zip File.."
                exit()
            except RuntimeError:
                pass
    print "Password not found.."

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    cracker()
