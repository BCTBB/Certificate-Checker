#!/usr/bin/python
import argparse
import ssl
import socket
import hashlib

parser = argparse.ArgumentParser(description='Certificate Thumbprint Tool')
parser.add_argument("-u", "--url", default="", help="Please provide a URL to check, "
                                                    "URL needs to be formatted like foo.foo.com ")

def certThumbCheck(passedurl):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    wrappedSocket = ssl.wrap_socket(sock)

    try:
        wrappedSocket.connect((passedurl, 443))
    except:
        # bad
        print "0"
    else:
        der_cert_bin = wrappedSocket.getpeercert(True)

        # Thumbprint
        thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
        print thumb_sha256

    wrappedSocket.close()

if "__name__" == "__main__":
    args = parser.parse_args()
    storedurl = args.url

    if storedurl == "":
        print "Please provide a url. URL needs to be formated like foo.foo.com"
        exit()
    else:
        certThumbCheck(str(storedurl))