#!/usr/bin/python3
#Import General Google API module
from apiclient.discovery import build
import sys,re

#Check if ISBN has been passed into program
if(len(sys.argv) == 1):
	print("Usage: ISBN.py ISBN_Number")
	sys.exit()
#Strip all non-numerals from ISBN
ISBN = re.sub("[^0-9]", "", sys.argv[1])

#Spawn the books API object
service = build('books', 'v1', developerKey="INSERT KEY HERE")
#Search for books matching ISBN
search = service.volumes().list(q="isbn:"+ISBN).execute()
#If none are found, exit
if(search["totalItems"] == 0):
	print("ISBN not found")
	sys.exit()
#Get information on the first result, which will be the book, since we're searching by ISBN
item = service.volumes().get(volumeId=search["items"][0]["id"]).execute()
#The category from the search is more general, so print that first
print("Main Categories: " + str(search["items"][0]['volumeInfo']["categories"]))
#The individual item result gives a finer category, so print that second
print("Sub Categories: " + str(item['volumeInfo']["categories"]))