#!/usr/bin/env python2

import json
import sys
import imaplib
import email
from watson_developer_cloud import VisualRecognitionV3
from BeautifulSoup import BeautifulSoup
import quopri
import uuid
import datetime
from pymongo import MongoClient

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='9f58a65ffdcc876c48a907966174efe1d395e374')
client = MongoClient('mongodb://admin:abcdef@ds117819.mlab.com:17819/mavericks')
db = client.get_default_database()
pictures = db['pictures']
M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    M.login('mavericks.sbhacks@gmail.com', 'qawsedrftg')
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")

M.select()

def databaseUpload(data):
	print(data)
	pictures.insert(data)

def objTranslate(jsonObj):
	if not jsonObj["images"][0]["classifiers"][0]["classes"]:
		return
	obj = {}
	obj['ID'] = str(uuid.uuid4())
	obj['address'] = jsonObj["images"][0]["resolved_url"]
	obj['link'] = 'www.google.com'
	obj['altText'] = "Image not found"
	obj['tags'] = []
	classes = jsonObj["images"][0]["classifiers"][0]["classes"]
	for tag in classes:
		obj['tags'].append(tag["class"])
	obj['time'] = datetime.datetime.now()
	databaseUpload(obj)

def imgRecognition(imgUrl):
	objTranslate(visual_recognition.classify(images_url=imgUrl, threshold=0.7))

def htmlToImgs(html):
	soup = BeautifulSoup(quopri.decodestring(html))
	tags = soup.findAll('img')
	srcs = []
	for each in tags:
		srcs.append(each['src']) 
	for url in srcs:
		imgRecognition(url)

def process_mailbox(M, mode="ALL"):
  rv, data = M.search(None, mode)
  if rv != 'OK':
      print("No messages found!")
      return

  for num in data[0].split():
      rv, data = M.fetch(num, '(RFC822)')
      if rv != 'OK':
          print("ERROR getting message", num)
          return

      msg = email.message_from_string(data[0][1])
      print 'Message %s: %s' % (num, msg['Subject'])
      if msg.is_multipart():
      	for payload in msg.get_payload():
      		#print payload.get_payload();
      		with open(str(num)+".html", 'w') as f:
      			#f.write(payload.get_payload())
      			if num == '6':
      				htmlToImgs(payload.get_payload())
      else:
      	f.write(msg.get_payload())

print("Processing mailbox...\n")
process_mailbox(M, "Unseen")

client.close()
M.close()
M.logout()