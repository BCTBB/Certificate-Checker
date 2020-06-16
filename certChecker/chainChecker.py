import collections
from datetime import datetime, timedelta
import time
import json
import requests
from shutil import copyfile
import os
import urllib2

urlArr = ['foo1.foo.com',
          'foo2.foo.com']

def dictionaryCheck():

    for i in urlArr:
        if i not in d:
            d[i] = {}
            d[i]['Status'] = ""
            print i, " has been added to dictionary"
        else:
            print i, " has already been cataloged in the dictionary"

        if d[i]['Status'] == '200':
            print i, d[i]['Status']
        elif d[i]['Status'] == '504':
            print i, d[i]['Status']
        elif d[i]['Status'] == '400':
            print i, d[i]['Status']
        elif d[i]['Status'] == '404':
            print i, d[i]['Status']
        else:
            print i, " does not have a status code"
            print "lets add one"
            checkURL(i)
            if d[i]['Status'] == "":
                print "Status is still NULL\n"
            else:
                checkCert(i)
        writeFile()


def checkURL(hostname):
    try:
        print "Trying to hit: ", hostname
        r = requests.get("https://" + hostname, timeout=3)
        try:
            print r.url
        except:
            print "Cannot print URL"
        try:
            print r.status_code
            d[hostname]['Status'] = r.status_code
        except:
            print "Cannot print status_code"
    except IOError:
        print "Cannot open https://" + hostname

def checkCert(hostname):
    req = urllib2.Request("https://" + hostname)
    try:
        urllib2.urlopen(req,timeout=3)
        d[hostname]["cert"] = "valid"
        print "valid cert\n"
    except urllib2.HTTPError, e:
        print e.code
        d[hostname]["cert"] = "connection bad"
    except urllib2.URLError, e:
        print e.args
        d[hostname]["cert"] = "invalid"
        print "invalid cert\n"
    except:
        d[hostname]["cert"] = "connection bad"
        print "connection bad\n"

def writeFile():
    data = collections.OrderedDict(sorted(d.items()))

    with open('output/info.json', 'wb') as output:
        json.dump(data, output, indent=4, sort_keys=True)

if os.path.isfile('output/info.json'):
    copyfile('output/info.json', 'input/info.json')
    # backup json
    copyfile('output/info.json', 'output/Backup/SSL-Checker' + time.strftime("%Y%m%d-%H%M%S") + '.json')
if os.path.isfile('input/info.json'):
    with open('input/info.json') as inp:
        d = json.loads(inp.read())
else:
    d = {}

if "__name__" == "__main__":
    dictionaryCheck()