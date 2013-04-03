bvvbot
======

BVV Bot

Cronjob anlegen
------------------
In Konsole: crontab -e

Stündlich zwischen 8 und 20 Uhr wird das Script aufgerufen:

8-20 * * * python XXX/bvvnkupdates.py

Bibliotheken
----------------------
twitter

https://github.com/sixohsix/twitter 

BeautifulSoup

http://www.crummy.com/software/BeautifulSoup/

Twitter Account
--------------------------
* neuen Twitteraccount für den Bot anlegen
* Twitter Anwendung erstellen https://dev.twitter.com/apps/new
* access token in Anwendung anlegen
* Dies in bvvnkupdates.py Kopieren: Consumer key, Consumer secret, access token und access tokensecret
