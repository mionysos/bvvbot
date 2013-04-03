#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#from risopen import *
import urllib2
from BeautifulSoup import BeautifulSoup
from twitter import *  #Bibliothek auf https://github.com/sixohsix/twitter 

# folgende Schluessel nach Erzeugen einer App auf Twitter erzeugt
CONSUMER_KEY = 		"XXX"								#consumer
CONSUMER_SECRET = 	"XXX"		#consumer secret
OAUTH_TOKEN  = 		"XXX"		#access token
OAUTH_SECRET  = 	"XXX"		#access token secret

# Datei für hoechste volfdnr
datei_volfdnr =		"bvvnkupdates/letzte_volfdnr.txt"

drucksachenquelle = 'http://www.berlin.de/ba-neukoelln/bvv-online/vo040.asp?showall=true&VO040FIL1=XIX'

def tweetsenden(tweettext):
	t = Twitter(auth=OAuth(OAUTH_TOKEN,OAUTH_SECRET,CONSUMER_KEY,CONSUMER_SECRET))
	t.statuses.update(status=tweettext) 

def letzte_volfdnr():
	# hoechste volfdnr, die zuletzt in Datei geschrieben wurde, wird ausgelesen
	text_file 		= open(datei_volfdnr, "r")
	letzte_volfdnr 	= text_file.read()
	text_file.close()
	return int(letzte_volfdnr)

def neue_volfdnr_in_datei_schreiben(neue_volfdnr):
	# neu ermittelte hoechste volfdnr wird in Datei geschrieben
	text_file 		= open(datei_volfdnr, "wb")
	text_file.write(str(neue_volfdnr)) 
	text_file.close()	

def hole_drucksachendict(drucksachenquelle):
	response = 			urllib2.urlopen(drucksachenquelle)
	html = 				response.read()
	soup = 				BeautifulSoup(html)
	# alle relevanten Daten befinden sich in Tabellenzeilen die 2 verschiedenen Klassen zugeordnet sind
	table = 			soup("tr", {'class' : 'zl11' })
	table2 = 			soup("tr", {'class' : 'zl12' })
	table+=				table2

	alle_volfdnr = 		[]
	drucksachendict = 	{}
	for entry in table:
		set={}
		set["titel"]=					entry.findAll('a')[0].string.encode('utf-8', 'ignore')
		set["initiator"]=				entry.findAll('td')[3].string.encode('utf-8', 'ignore')
		set["drucksachenart"]= 			entry.findAll('td')[5].string.encode('utf-8', 'ignore')
		set["link"]=					entry.a['href'].encode('utf-8', 'ignore')
		drucksachendict[str(entry.td.form.input['value'])]=set
		alle_volfdnr.append(entry.td.form.input['value'])
	return drucksachendict

letzte_volfdnr 	= letzte_volfdnr()
alledrucksachen = hole_drucksachendict(drucksachenquelle)	# Dictionary mit Drucksachen durch Parsen erstellt
neue_volfndr 	= []	# alle neuen volfdnr werden zwischengespeichert

# sukkzessiv werden alle Drucksachen mit dem Key volfdnr 
for volfdnr in alledrucksachen.keys():
	if int(volfdnr)>letzte_volfdnr:	# 
		neue_volfndr.append(int(volfdnr))
		tweet_drucksachenart = 	alledrucksachen[volfdnr]["drucksachenart"]
		tweet_initiator = 		alledrucksachen[volfdnr]["initiator"]
		tweet_titel = 			alledrucksachen[volfdnr]["titel"].split("&nbsp;")[1]
		tweet_link = 			alledrucksachen[volfdnr]["link"]
		# Zusammensetzen des Tweets
		tweettext = tweet_drucksachenart+"/"+tweet_initiator+": "+tweet_titel+" http://www.berlin.de"+tweet_link+" #bvvnk"
		# Überprüfung der Textlängenbegrenzung und ggf gekürzt neu zusammengesetzt
		if len(tweettext)>144:
			differenz = 		len(tweettext)-175
			len_tweet_titel = 	len(tweet_titel)-differenz
			tweet_titel = 		tweet_titel[:len_tweet_titel]+"..."
		tweettext = tweet_drucksachenart+"/"+tweet_initiator+": "+tweet_titel+" http://www.berlin.de"+tweet_link+" #bvvnk"
		try:
			tweetsenden(tweettext) # Fehler beim Senden einzelner Tweets sollen nicht vom Senden weiterer abhalten
		except:
			pass

if len(neue_volfndr)>0:
	neue_volfdnr_in_datei_schreiben(max(neue_volfndr))


