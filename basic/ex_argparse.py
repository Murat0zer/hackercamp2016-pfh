#!/usr/local/bin/python
import argparse
import sys


description = """
    argparse basic example
    Example: python ex_argparse.py --domain http://example.com
"""

parser = argparse.ArgumentParser("example", description)
parser.add_argument("--domain", "-d", help="domain", required=True)
args = parser.parse_args()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    print args.domain
