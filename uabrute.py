#!/usr/bin/python2.7

import sys
import urllib2
import hashlib
import re
from argparse import ArgumentParser
import itertools
from operator import itemgetter
import os
import time
import datetime

parser = ArgumentParser()
parser.add_argument("-u", "--url", help="UABrute.py -url https://example.com.", required=True)
parser.add_argument("-d", "--downloadallfiles", help=" UABrute.py -url https://example.com --downloadallfiles",
    required=False, action='store_true')
args = parser.parse_args()


def tee(text):
    print text
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open("UA_BruteLogfile.log", 'a+') as f:
	f.write(st + " " + text + "\n")


def makedir(folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return final_directory


def hashvar(var):
    m = hashlib.md5()
    m.update(var)
    r = m.hexdigest()
    return r

def webwrite(url,d,hashsum,html):
    if d is True:
	webdownloads = "sitedownloads"
        if os.path.exists(webdownloads):
	    pass
	else:
	    makedir(webdownloads)
	site = re.sub("http.+//", "", url)
        site = re.sub("\/.+", "", site)
        #print site
        ndir = makedir(webdownloads + os.sep + site)
        #tee("Downloading " + str(url) + " with user agent " + str(ua))
        with open(ndir + os.sep +  hashsum, 'w') as f:
            f.write(html)

def downloader(url,ua,d):
    # type: (object, object) -> object
    headers = {'User-Agent': ua}
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    headercode = resp.getcode()
    html = resp.read()
    hashsum = hashvar(html)
    if d is True:
        webwrite(url,d,hashsum,html)
    tee("Site returned code: " + str(headercode) + " with User Agent: " + str(ua) + ' with hash: ' + str(hashsum) )
    return html


def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    try:
        if reply[0] == 'y':
            return True
    	if reply[0] == 'n':
            return False
    except IndexError as error:
            return yes_or_no(question)


def browserinfoparse(d):
    ualist = "UA.list"
    fileCreation = os.path.getctime(ualist)
    now = time.time()
    twodays_ago = now - 60*60*24*2 # Number of seconds in two days
    if fileCreation < twodays_ago:
       ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
       url = 'http://www.browser-info.net/useragents'
       d = False
       browserinfo = downloader(url, ua, d)
       if len(browserinfo) == 0:
           print(url + 'is no longer available - using cached UA.list.')
           #sys.exit()
       else:
           tee("Pulling list of most commonly utilized User Agent Strings.")
       ua_list = []
       spbrowserinfo = browserinfo.split("<")
       for i in spbrowserinfo:
           if 'useragent?q=' in i:
               line = re.sub('^.+>', '', i)
               if len(line) != 0:
                   ua_list.append(line.rstrip())
		   #with open("UA.lst", 'a+') as f:
        	   #    f.write(line + "\n")
       lines = list(line for line in ua_list if line)
       with open(ualist, 'w') as f:
           for line in lines:
               f.write(line + '\n') 
    else:
        with open(ualist) as f:
            ua_list = list(line.strip() for line in f.readlines())
    return ua_list

def iterator(site_list,d):
    totalUserAgentStrings = len(site_list)
    tee( "{0} user agents downloaded.".format(str(totalUserAgentStrings)))
    sorted_site = sorted(site_list, key=itemgetter('hashsum'))
    sorted_list = []
    for key, group in itertools.groupby(sorted_site, key=lambda x: x['hashsum']):
        sorted_list.append(list(group))
    #print sorted_list
    for slist in sorted_list:
	if d == True:
            downloader(args.url, slist[0], True)
        elif d == False:
            if len(slist) == 1:
                tee("Unique response received from user agent string.")
                tee(str(slist))
                download = yes_or_no("Do you want to download the site with this user agent?")
                if download == True:
                    downloader(args.url, slist[0], download)
                else:
                    pass
            elif len(slist) == totalUserAgentStrings:
                tee("No unique response from site based on user agent string.")
                download = yes_or_no("Do you want to download the site?")
                if download == True:
                    downloader(args.url, slist[0], download)
                else:
                    pass
            else:
		pass


def main():
    # Iterate over UserAgents
    if args.downloadallfiles is None:
        d = False
    else:
        d = True
    
    userAgents = browserinfoparse(d)
    print("")
    tee("Initating requests against " + args.url + " with found user agent strings.")
    print("")
    #print(userAgents)
    site_list = []
    for userAgent in userAgents:
	#print(userAgent)
	try:
            htm = downloader(args.url, userAgent, "False")
            hashsum = hashvar(htm)
            site_list.append({'userAgent': userAgent, 'hashsum': hashsum})
        except:
            pass
    #print len(site_list)
    iterator(site_list,args.downloadallfiles)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        tee("Exiting....")
        sys.exit()
