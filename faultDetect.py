#!/usr/bin/python

import MySQLdb
import smtplib
import urllib2
import datetime
import xml.etree.cElementTree as ET



def sendEmail():
	fromaddr = 'gkyrtsakas@gmail.com'
	toaddrs  = ['gkyrtsakas@gmail.com']
	msg = "\r\n".join([
	  "From: gkyrtsakas@gmail.com",
	  "To: gkyrtsakas@gmail.com",
	  "Subject: Just a message",
	  "",
	  "Daily Solar Report",
	  faultString
	  ])
	username = 'gkyrtsakas@gmail.com'
	password = 'uriuxezdztdqxozp'
	
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


flag = False
cFaultCount = 0 #row[2]
v1FaultCount = 0 #row[1]
v2FaultCount = 0 #row[3]
[sr,ss] = getSRSS()
dt = datetime.datetime.now()
faultString = ""
db = MySQLdb.connect("localhost", "root", "root", "mysql")
cursor = db.cursor()
try:
	cursor.execute("SELECT * FROM data1 WHERE (DAY(date) = DAY(NOW()) AND (MONTH(date)) = MONTH(NOW()))")
	results = cursor.fetchall()
	for row in results:
		v1 = row[1]
		v2 = row[3]
		vt = row[4]
		c = row[2]
		tm = row[0].strftime("%H:%M:%S")
		if (tm > sr and tm < ss):
			if (c < 0.2):
				cFaultCount += 1
			if (v2*0.7 > v1):
				v1FaultCount += 1
			if (v1*0.7 > v2):
				v2FaultCount += 1


except:
	print "Error: unable to connect to db"

if (cFaultCount > 0):
	faultString+="A current fault has been detected. Please Inspect.\r\n"
if (v1FaultCount > 0):
	faultString+="Panel 1 may be faulty. Please inspect.\r\n"
if (v2FaultCount > 0):
	faultString+="Panel 2 may be faulty. Please inspect.\r\n"

print faultString
sendEmail()	
db.close()



