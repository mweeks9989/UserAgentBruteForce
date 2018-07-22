#!/usr/bin/python
import sys
import urllib2
import hashlib
import re
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-u", "--url", help="UABrute.py -url https://example.com.", required=True)

args = parser.parse_args()

def hashvar(var):
    m = hashlib.md5()
    m.update(var)
    r = m.hexdigest()
    print(r)

def downloader(url,UA):
    headers = {'User-Agent': UA}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    print "Downloading " + url
    return html

def browserinfoparse():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    url = 'http://www.browser-info.net/useragents'
    browserinfo = downloader(url,ua)
    ua_list = []
    spbrowserinfo = browserinfo.split("<")
    for i in spbrowserinfo:
        if 'useragent?q=' in i:
            line = re.sub('^.+>', '', i)
            if len(line) != 0:
                ua_list.append(line)
    return ua_list

def main():
    # Iterate over UserAgents
    uas = browserinfoparse()
    for ua in uas:
        print ua
        print args.url
        try:
            htm = downloader(args.url, ua)
            hashvar(htm)
        except:
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting...."
        sys.exit()


