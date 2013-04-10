#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import pickle

from parameter import *
import urllib2
from BeautifulSoup import BeautifulSoup  # HTML Parser
from twitter import *					# Bibliothek auf https://github.com/sixohsix/twitter 

# folgende Schluessel nach Erzeugen einer App auf Twitter erzeugt ( @BVVupdates )
CONSUMER_KEY 		= "XXX"									#consumer
CONSUMER_SECRET 	= "XXX"			#consumer secret
OAUTH_TOKEN 		= "XXX"	#access token
OAUTH_SECRET  		= "XXX"			#access token secret

def hole_drucksachendict(drucksachenquelle):
	response 		= urllib2.urlopen(drucksachenquelle)
	#print response.headers['content-type']
	html 			= response.read()
	html = unicode(html, "iso-8859-1")	
	soup 			= BeautifulSoup(html)
	# alle relevanten Daten befinden sich in Tabellenzeilen die 2 verschiedenen Klassen zugeordnet sind
	table 			= soup("tr", {'class' : 'zl11' })
	table2 			= soup("tr", {'class' : 'zl12' })
	table			+=table2

	drucksachendict = {}
	for entry in table:
		set={}
		try:
			set["titel"]			= entry.findAll('a')[0].string.encode('utf-8', 'ignore')
		except:
			set["titel"]			= ""
		try:
			set["initiator"]		= entry.findAll('td')[3].string.encode('utf-8', 'ignore')
		except:
			set["initiator"]		= ""
		try:
			set["drucksachenart"]	= entry.findAll('td')[5].string.encode('utf-8', 'ignore')
		except:
			set["drucksachenart"]	= ""
		set["link"]				= entry.a['href'].encode('utf-8', 'ignore')
		#print set
		if not "NPD" in set["initiator"]:
			drucksachendict[int(entry.td.form.input['value'])] = set
		else:	
			print "NPD: "+str(entry.td.form.input['value'])
	return drucksachendict

def tweetsenden(tweettext):
	t 				= Twitter(auth=OAuth(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET))
	#tweettext = unicode( tweettext, "utf-8" )
	t.statuses.update(status=tweettext) 

def komponiere_tweettext(bezirksschluessel,drucksache):
	
	tweet_drucksachenart 	= drucksache["drucksachenart"]
	tweet_initiator 		= drucksache["initiator"]
	tweet_titel 			= drucksache["titel"].split("&nbsp;")[1] # noch unschöne Stelle
	tweet_titel.replace('&ndash;', '')
	tweet_link 				= drucksache["link"]
	# Zusammensetzen des Tweets: 1. Versuch
	tweet_bezirk = bezirke[bezirksschluessel][2]
	tweettext = tweet_drucksachenart+" - "+tweet_initiator+" in "+tweet_bezirk+": "+tweet_titel+" http://www.berlin.de"+tweet_link
	if len(tweettext)>141:
		differenz 		= len(tweettext)-175
		len_tweet_titel = len(tweet_titel)-differenz
		tweet_titel 	= tweet_titel[:len_tweet_titel]+"..."
	# Zusammensetzen des Tweets: 2. Versuch
	tweettext = tweet_drucksachenart+" - "+tweet_initiator+" in "+tweet_bezirk+": "+tweet_titel+" http://www.berlin.de"+tweet_link
	return tweettext


import pickle
letzte_volfdnr = pickle.load(open('letzte_volfdnr.p', 'rb'))

print letzte_volfdnr

for bezirksschluessel in bezirke.keys():
	drucksachenquelle = 'http://www.berlin.de/'+bezirke[bezirksschluessel][0]+'/bvv-online/vo040.asp'+bezirke[bezirksschluessel][3]
	drucksachendict = hole_drucksachendict(drucksachenquelle)
	alle_volfdnr = drucksachendict.keys()
	neue_volfndr = []
	for volfdnr in alle_volfdnr:
		if int(volfdnr)>letzte_volfdnr[bezirksschluessel]:
			neue_volfndr.append(int(volfdnr))
			drucksache = drucksachendict[volfdnr]
			tweettext = komponiere_tweettext(bezirksschluessel,drucksache)
			print tweettext
			try:
				tweetsenden(tweettext)
				print "tweet gesendet"
			except:
				print "tweet nicht gesendet"
				pass
			print volfdnr,bezirksschluessel
	if len(neue_volfndr)>0:
		letzte_volfdnr[bezirksschluessel]=max(neue_volfndr)
print letzte_volfdnr 

pickle.dump(letzte_volfdnr, open('letzte_volfdnr.p', 'wb'))
