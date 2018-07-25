#!/usr/bin/python

import sys
import urllib2
import hashlib
import re
from argparse import ArgumentParser
import itertools
from operator import itemgetter

parser = ArgumentParser()
parser.add_argument("-u", "--url", help="UABrute.py -url https://example.com.", required=True)

args = parser.parse_args()


def hashvar(var):
    m = hashlib.md5()
    m.update(var)
    r = m.hexdigest()
    return str(r)

def downloader(url,UA):
    # type: (object, object) -> object
    headers = {'User-Agent': UA}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    print "Downloading " + url + " with user agent " + UA
    return html

def browserinfoparse():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    url = 'http://www.browser-info.net/useragents'
    browserinfo = downloader(url, ua)
    if len(browserinfo) == 0:
        print url + 'is no longer available please contact author.'
        sys.exit()
    else:
        print "Pulling list of most commonly utilized User Agent Strings."
    ua_list = []
    spbrowserinfo = browserinfo.split("<")
    for i in spbrowserinfo:
        if 'useragent?q=' in i:
            line = re.sub('^.+>', '', i)
            if len(line) != 0:
                ua_list.append(line)
    return ua_list

def iterator(site_list):
    totalUserAgentStrings = len(site_list)
    print str(totalUserAgentStrings) + " user agents downloaded."

    sorted_site = sorted(site_list, key=itemgetter('hashsum'))
    sorted_list = []
    for key, group in itertools.groupby(sorted_site, key=lambda x: x['hashsum']):
        sorted_list.append(list(group))

    for slist in sorted_list:
        if len(slist) == 1:
            print "Unique response received from user agent string."
            print slist
        elif len(slist) == totalUserAgentStrings:
            print "No unique response from site based on user agent string."
        else:
            print "Multiple responses based on multiple user agent strings."


def main():
    # Iterate over UserAgents
    userAgents = browserinfoparse()
    print ""
    print "Initating requests against " + args.url + " with found user agent strings."
    print ""
    site_list = []
    for userAgent in userAgents:
        try:
            htm = downloader(args.url, userAgent)
            hashsum = hashvar(htm)
            site_list.append( {'userAgent':userAgent, 'hashsum':hashsum})
        except:
            pass
    iterator(site_list)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting...."
        sys.exit()

