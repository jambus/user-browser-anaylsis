#!/usr/bin/env python3

import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt

def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print ("URL format error!")

def analyze(results):

    prompt = input("[.] Type <c> to print or <p> to plot\n[>] ")

    if prompt == "c":
        for site, count in results.items():
            print (site, count)
    elif prompt == "p":
        plt.bar(range(len(results)), results.values(), align='edge')
        plt.xticks(rotation=45)
        plt.xticks(range(len(results)), results.keys())
        plt.show()
    else:
        print ("[.] Uh?")
        quit()

def getOSSystemType():
	osName =  os.name
	if osName == 'posix':
		return 'MAC'
	elif osName == 'nt':
		return 'WINDOWS'
	else:
		return 'OTHER' 

def loadBrowserHistory():
	osType = getOSSystemType()

	#path to user's history database (Chrome)
	if osType == 'MAC':
		data_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default'
	elif osType == 'WINDOWS':
		data_path = os.path.expanduser('~')+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
	else:
		print ('Unsupported OS type, exit...')
		quit()

	files = os.listdir(data_path)
	history_db = os.path.join(data_path, 'history')
	
	#querying the db
	c = sqlite3.connect(history_db)
	cursor = c.cursor()
	select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
	cursor.execute(select_statement)
	
	results = cursor.fetchall() #tuple
	cursor.close()
	c.close()

	return results

def convertHistoryRecordsToDict(results):
	sites_count = {} #dict makes iterations easier :D

	for url, count in results:
	    url = parse(url)
	    if url in sites_count:
	        sites_count[url] += 1
	    else:
	        sites_count[url] = 1

	sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
	return sites_count_sorted

results = loadBrowserHistory()
analyze (convertHistoryRecordsToDict(results))