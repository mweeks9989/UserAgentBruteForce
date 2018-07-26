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
parser.add_argument("-d", "--downloadallfiles", help=" UABrute.py -url https://example.com --downloadallfiles",
    required=False, type=bool)
args = parser.parse_args()


def hashvar(var):
    m = hashlib.md5()
    m.update(var)
    r = m.hexdigest()
    return r


def downloader(url,ua,d):
    # type: (object, object) -> object
    headers = {'User-Agent': ua}
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    if d is True:
        site = re.sub("^.+\:", "", url)
        print("Downloading " + str(url) + " with user agent " + str(ua))
        with open('site', 'w') as f:
            f.write(html)
    return html


def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


def browserinfoparse(d):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    url = 'http://www.browser-info.net/useragents'
    browserinfo = downloader(url, ua, d)
    if len(browserinfo) == 0:
        print(url + 'is no longer available please contact author.')
        sys.exit()
    else:
        print("Pulling list of most commonly utilized User Agent Strings.")
    ua_list = []
    spbrowserinfo = browserinfo.split("<")
    for i in spbrowserinfo:
        if 'useragent?q=' in i:
            line = re.sub('^.+>', '', i)
            if len(line) != 0:
                ua_list.append(line)
    return ua_list


def iterator(site_list):
    totalUserAgenStrings = len(site_list)
    print "{0} user agents downloaded.".format(str(totalUserAgenStrings))
    sorted_site = sorted(site_list, key=itemgetter('hashsum'))
    sorted_list = []
    for key, group in itertools.groupby(sorted_site, key=lambda x: x['hashsum']):
        sorted_list.append(list(group))
    for slist in sorted_list:
        if len(slist) == 1:
            print("Unique response received from user agent string.")
            print(slist)
            download = yes_or_no("Do you want to download the site with this user agent? y/n")
            if download == True:
                downloader(args.url, slist[0], download)
            else:
                pass
        elif len(slist) == totalUserAgentStrings:
            print("No unique response from site based on user agent string.")
            download = yes_or_no("Do you want to download the site with this user agent? y/n")
            if download == True:
                downloader(args.url, slist[0], download)
            else:
                pass
        else:
            print("Multiple responses based on multiple user agent strings.")


def main():
    # Iterate over UserAgents
    if args.downloadallfiles is None:
        d = False
    else:
        d = True
    userAgents = browserinfoparse(d)
    print("")
    print("Initating requests against " + args.url + " with found user agent strings.")
    print("")
    site_list = []
    for userAgent in userAgents:
        try:
            htm = downloader(args.url, userAgent, d)
            hashsum = hashvar(htm)
            site_list.append({'userAgent': userAgent, 'hashsum': hashsum})
        except:
            pass
    print site_list
    iterator(site_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit()
