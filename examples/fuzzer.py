#!/usr/local/bin/python
import argparse
import sys
import requests
import os
from termcolor import colored

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_WORD_LIST = os.path.join(SCRIPT_PATH, "wordlist", "admin-panels.txt")
COLOR = {404: "red", 200: "green", 301: "blue", 302: "blue"}

description = """
    This fuzzer script has been writed for hackercamp
    Example: python fuzzer.py --url http://example.com/FUZZER --hc 404 --wordlist /home/user/wordlist.txt
"""

parser = argparse.ArgumentParser("fuzzer", description)
parser.add_argument("--wordlist", "-w", help="wordlist path, format:/home/user/wordlist.txt", default=DEFAULT_WORD_LIST)
parser.add_argument("--url", "-u", help="fuzzing url, format: http://www.example.com/FUZZ", required=True)
parser.add_argument("--hc", help="ignore http response", default="")
args = parser.parse_args()


def get_color(code):
    try:
        return COLOR[code]
    except KeyError:
        return "white"


def fuzzing():
    if not args.url.endswith("FUZZ"):
        print "Please enter url this format: http://www.example.com/FUZZ"
        exit(0)
    url = args.url.split('FUZZ')[0]
    args.hc = args.hc.split(",")
    print """
====================
Response    Request
====================
    """
    with open(args.wordlist, "r") as f:
        for line in f.readlines():
            line = line.strip()

            try:
                req = requests.head("{}{}".format(url, line))
            except requests.exceptions.ConnectionError:
                print "Connection Error.."
                exit(0)

            if str(req.status_code) in args.hc:
                sys.stdout.write('\x1b[K{}         {}\r'.format(colored(req.status_code, get_color(req.status_code)),
                                                                line))
            else:
                sys.stdout.write('{}         {}\n'.format(colored(req.status_code, get_color(req.status_code)), line))
            sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    fuzzing()
