#!/usr/bin/python

import MySQLdb
import smtplib
import urllib2
import datetime
import xml.etree.cElementTree as ET

db = MySQLdb.connect("localhost", "root", "root", "mysql")
cursor = db.cursor()
try:
	cursor.execute("SELECT * FROM data1 WHERE (DAY(date) = DAY(NOW()) AND (MONTH(date)) = MONTH(NOW()))")
	results = cursor.fetchall()
	for row in results:
		print row
except:
	print "Error: unable to connect to db"
db.close()

message = 	"""From: From Person <from@fromdomain.com>
			To: To Person <to@todomain.com>
			MIME-Version: 1.0
			Content-type: text/html
			Subject: SMTP HTML e-mail test

			This is an e-mail message to be sent in HTML format

			<b>This is HTML message.</b>
			<h1>This is headline.</h1>"""


fromaddr = 'gkyrtsakas@gmail.com'
toaddrs  = ['gkyrtsakas@gmail.com']
msg = "\r\n".join([
  "From: gkyrtsakas@gmail.com",
  "To: gkyrtsakas@gmail.com",
  "Subject: Just a message",
  "",
  "Why, oh why"
  ])
username = 'gkyrtsakas@gmail.com'
password = 'uriuxezdztdqxozp'
"""
try:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.close()
	print "mail sent"
except:
	print "failed to send mail"
"""

#http://www.earthtools.org/sun/<latitude>/<longitude>/<day>/<month>/<timezone>/<dst>

def getSRSS():
	dt = datetime.datetime.now()
	timezone = "-5/"
	latitude = "42.088032/"
	longitude = "-82.705078/"
	day = ("%s/" %dt.day)
	month = ("%s/" %dt.month)

	url = "http://www.earthtools.org/sun/" + latitude + longitude + day + month + timezone + "0"

	result = urllib2.urlopen(url).read()

	root = ET.fromstring(result)

	sunrise = root[3][0].text

	sunset = root[4][0].text

	return [sunrise, sunset]
