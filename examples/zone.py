import dns.resolver
import dns.query
import dns.zone
import socket
import dns.exception
import argparse
import sys

description = """
    Zone transfer script for hackercamp
    Example: python zone.py --domain <domain>
"""

parser = argparse.ArgumentParser("zone transfer", description)
parser.add_argument("--domain", "-d", help="domain, format:example.com", required=True)
args = parser.parse_args()


def get_ns(domain):
    try:
        name_servers = dns.resolver.query(domain, 'NS')
        return name_servers
    except dns.resolver.NoNameservers:
        print "Domain: {} has no ns records.".format(domain)
    except dns.resolver.NXDOMAIN:
        print "Non-existent domain: {}".format(domain)
    except dns.exception.Timeout:
        print "Timeout"
    except dns.resolver.NoAnswer:
        print "Problem getting NS record"
    exit()


def zone(domain):
    for name_server in get_ns(domain):
        print "Trying for {}".format(name_server)
        try:
            xfer = dns.zone.from_xfr(dns.query.xfr(str(name_server), domain))
            names = xfer.nodes.keys()
            names.sort()
            with open('zone.txt', 'w') as f:
                for n in names:
                    f.write(xfer[n].to_text(n))
            print "Zone transfer has been found for {}. Result has been writed zone.txt".format(name_server)
            exit()
        except dns.zone.NoNS:
            print "Domain: {} exists, but has no ns records..".format(domain)
        except dns.resolver.NXDOMAIN:
            print "Domain: unresponsive, try again"
        except dns.exception.FormError:
            print "Xfer refused.."
        except EOFError:
            print "EOFError"
        except KeyboardInterrupt:
            print "User cancelled"
        except KeyError as e:
            print "KeyError {}".format(e)
        except socket.error:
            print "Failed: connection refused"
    print "Zone transfer not found.."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print parser.print_help()
        exit()
    zone(args.domain)
