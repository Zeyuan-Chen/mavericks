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
import time

visual_recognition = VisualRecognitionV3('2017-06-22', api_key='93b477cab6e97e71c6e83c344f36c65eeb60cc96')
client = MongoClient('mongodb://admin:abcdef@ds117819.mlab.com:17819/mavericks')
db = client.get_default_database()
pictures = db['pictures']
M = imaplib.IMAP4_SSL('imap.gmail.com')
brands = ["nike", "adidas", "kohls", "timberland", "asos", "asics", "uniqlo", "diesel"]

try:
    M.login('mavericks.sbhacks@gmail.com', 'qawsedrftg')
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")

M.select()

def databaseUpload(data):
	print(data)
	pictures.insert(data)

def objTranslate(jsonObj, linkUrl):
	if not jsonObj["images"][0]["classifiers"][0]["classes"]:
		return
	obj = {}
	obj['ID'] = str(uuid.uuid4())
	obj['address'] = jsonObj["images"][0]["resolved_url"]
	obj['link'] = linkUrl
	obj['altText'] = "Image not found"
	obj['tags'] = []
	classes = jsonObj["images"][0]["classifiers"][0]["classes"]
	for tag in classes:
		obj['tags'].append(tag["class"])
	for brand in brands:
		if brand in obj['link']:
			obj['tags'].append(brand)
			break
	obj['time'] = datetime.datetime.now()
	databaseUpload(obj)

def imgRecognition(imgUrl, linkUrl):
	objTranslate(visual_recognition.classify(images_url=imgUrl, threshold=0.8), linkUrl)

def htmlToImgs(html):
	soup = BeautifulSoup(quopri.decodestring(html))
	tags = soup.findAll('img')
	srcs = []
	for each in tags:
		tmp = each.parent
		while tmp.name != 'a' and tmp != soup:
			tmp = tmp.parent
		if tmp != soup:
			srcs.append((each['src'], tmp['href']))
		else:
			srcs.append((each['src'], ""))
	for url in srcs:
		if url[1] == "":
			continue
		imgRecognition(url[0], url[1])

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
      		htmlToImgs(payload.get_payload())

while True:
	print("Processing mailbox...\n")
	process_mailbox(M, "Unseen")
	print("Processing finished")
	time.sleep(300)

client.close()
M.close()
M.logout()