#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Parameter
#-----------


mysql_host =   			"localhost"
mysql_user = 			"XXX"
mysql_passwd = 			"YYY"
mysql_db = 				"ZZZ"

 
bezirke = {
		# 	URL-Bestandteil						Name in Schoenform				Kurzform	Quellenparameter
		"tk":["ba-treptow-koepenick",			"Treptow-Köpenick",				"TrKö",		""],
		"ts":["ba-tempelhof-schoeneberg",		"Tempelhof-Schöneberg",			"TSch",		""],
		"sz":["ba-steglitz-zehlendorf",			"Steglitz-Zehlendorf",			"StZe",		""],
		"sp":["ba-spandau",						"Spandau",						"Span",		""],
		"re":["ba-reinickendorf",				"Reinickendorf",				"Rein",		""],
		"pa":["ba-pankow",						"Pankow",						"Pank",		""],
		"nk":["ba-neukoelln",					"Neukölln",						"Neuk",		"?showall=true&VO040FIL1=XIX"],
		"mi":["ba-mitte",						"Mitte",						"Mitt",		""],
		"mh":["ba-marzahn-hellersdorf",			"Marzahn-Hellersdorf",			"MaHe",		""],
		"li":["ba-lichtenberg",					"Lichtenberg",					"Lich",		"?showall=true&VO040FIL1=VII"],
		"fk":["ba-friedrichshain-kreuzberg",	"Friedrichshain-Kreuzberg",		"FrKr",		""],
		"cw":["ba-charlottenburg-wilmersdorf",	"Charlottenburg-Wilmersdorf",	"ChWi",		""]		}
		


scripe_in_url = [
		"vo020.asp",
		"vo040.asp?showall=true", 	# Drucksachenliste: VOLFDNR, Name, Initiator, Abschl, D.-Art
		"pa021.asp", 				# aktuelle BV: Name, Art der Mitarbeit, Herkunft, seit
		"kp020.asp",
		"au010.asp", 				# Ausschuesse: Name, Mitglieder, Letzte Sitzung, Naechste Sitzung 
		"au020.asp",
		"fr010.asp", 				# Fraktionen: Name, Mitglieder, Letzte Sitzng, Naechste Sitzung
		"fr020.asp",
		"to010.asp",				# Tagesordnung eines to010.asp?SILFDNR=1058&options=4
		"ka040.asp?showall=true", 	# Kleine Anfragen: Nummer, Betreff, Eingang, Antwort
		"si010.asp", 				# Sitzungskalender
		"si018.asp"] 				# Sitzung Suchen

muster_drucksache =		{	"titel":"Drucksache - VII/0401",
							"betreff":"Schulweg der Schmöckwitzer Inselschule sichern",
							"status":"öffentlich",
							"ursprung_initiator":"SPD",
							"ursprung_verfasser":"Rick Nagelschmidt",	
							"ursprung_drucksacheart":"Antrag",
							"aktuell_initiator":"SPD",
							"aktuell_verfasser":"",
							"aktuell_drucksacheart":"Antrag",
							"beteiligt":"CDU",
							"text":"ganz viel Antragstext, der Übersicht halber weggelassen",
							"beratungsfolge":
								[{	"silfdnr":"3594",
									"gremium":"BVV Treptow-Köpenick",
									"datum":"21.03.13",
									"gremientermin":"17. (öffentliche) Sitzung der Bezirksverordnetenversammlung",
									"status":"Entscheidung überwiesen"},
								{	"silfdnr":"3747",
									"gremium":"Ausschuss für Bürgerdienste und Ordnungsangelegenheiten",
									"datum":"11.04.13",
									"gremientermin":"14. (öffentliche) Sitzung des Ausschusses für Bürgerdienste und Ordnungsangelegenheiten",
									"status":"Empfehlung"},		
								{	"silfdnr":"",
									"gremium":"BVV Treptow-Köpenick",
									"datum":"",
									"gremientermin":"",
									"status":"Entscheidung"}]}	
