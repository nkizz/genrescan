#!/usr/local/bin/python3
#Import General Google API module
from apiclient.discovery import build
import sys,re
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
#Spawn the books API object
service = build('books', 'v1', developerKey="***REMOVED***")

def lookup():
	#Strip all non-numerals from ISBN
	ISBN = re.sub("[^0-9]", "", ISBNEdit.text())
	ISBNEdit.setText("")
	#Search for books matching ISBN
	search = service.volumes().list(q="isbn:"+ISBN).execute()
	#If none are found, exit
	if(search["totalItems"] == 0):
		title.setText("ISBN not found")
		category.setText("")
		subCategory.setText("")
		return()
	#Get information on the first result, which will be the book, since we're searching by ISBN
	item = service.volumes().get(volumeId=search["items"][0]["id"]).execute()
	title.setText(item['volumeInfo']["title"])
	#The category from the search is more general, so print that first
	category.setText(", ".join(search["items"][0]['volumeInfo']["categories"]))
	#The individual item result gives a finer category, so print that second
	subCategory.setText(", ".join(item['volumeInfo']["categories"]))
#Setup font properties
smallFont = QFont("Ubuntu", 18)
largeFont = QFont("Ubuntu", 54)
#Configure widgets that need to be accessed later
title = QLabel("", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
category = QLabel("", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
subCategory = QLabel("", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
ISBNEdit = QLineEdit("0060512806", alignment=Qt.AlignCenter)
ISBNButton = QPushButton("Lookup")
#Add everything to the layout
layout.addWidget(QLabel("Title", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(title)

layout.addWidget(QLabel("Category", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(category)

layout.addWidget(QLabel("Sub-Category", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(subCategory)

layout.addWidget(ISBNEdit)
layout.addWidget(ISBNButton)
#Connect buttons to the function
ISBNEdit.returnPressed.connect(lookup)
ISBNButton.clicked.connect(lookup)

window.setLayout(layout)
window.show()
window.setWindowState(Qt.WindowMaximized)
app.exec_()

