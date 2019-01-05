#!/usr/bin/env python3
# Import General Google API module
from apiclient.discovery import build
import sys,re
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
app = QApplication([])
window = QMainWindow()
layout = QVBoxLayout()

#  Get the developer key from key.txt
try:
	with open("key.txt", "r") as file:
		developer_key = file.read()
# If there's an error, tell the user and exit
except FileNotFoundError:
	print("API Key Not Found")
	sys.exit(1)
# Spawn the books API object
try:
	service = build("books", "v1", developerKey=developer_key)
# Again, if there's an error, tell the user and exit
except:
    print("Error with accessing Google Books API.")
    print("Make sure developer key is correct.")
    sys.exit(1)

def lookup():
	'''
	This function takes the ISBN number the user entered
	and gets the title, category and subcategories of
	the book with that ISBN number.
	'''
	# Strip all non-numerals from ISBN
	ISBN = re.sub("[^0-9]", "", ISBNEdit.text())
	ISBNEdit.setText("")
	# If the user has not entered any number, don't do anything
	if len(ISBN) == 0:
		return
	# Search for books matching ISBN
	search = service.volumes().list(q="isbn:"+ISBN).execute()
	# If none are found, exit
	if search["totalItems"] == 0:
		title.setText("ISBN not found")
		category.setText("")
		subCategory.setText("")
		return
	# Get information on the first result,
	# which will be the book we are looking for,
	# since we're searching by ISBN.
	item = service.volumes().get(volumeId=search["items"][0]["id"]).execute()
	title.setText(item["volumeInfo"]["title"])
	# The category from the search is more general, so print that first
	try:
		category.setText(
			", ".join(search["items"][0]["volumeInfo"]["categories"])
		)
	# If an error occurs, then no category was found
	except KeyError:
		category.setText("No Category")
	# The individual item result gives a finer category, so print that second
	try:
		subCategory.setText(", ".join(item["volumeInfo"]["categories"]))
	# If an error occurs, then no sub-category was found
	except KeyError:
		subCategory.setText("No Sub-Category")

# Setup font properties
smallFont = QFont("Ubuntu", 18)
largeFont = QFont("Ubuntu", 54)
# Configure widgets that need to be accessed later
title = QLabel("Insert ISBN Number Below", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
category = QLabel("", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
subCategory = QLabel("", font=largeFont, alignment=Qt.AlignCenter, wordWrap=True)
ISBNEdit = QLineEdit("", placeholderText="ISBN Number", alignment=Qt.AlignCenter)
ISBNButton = QPushButton("Lookup")
# Add everything to the layout
layout.addWidget(QLabel("Title", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(title)

layout.addWidget(QLabel("Category", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(category)

layout.addWidget(QLabel("Sub-Category", font=smallFont, alignment=Qt.AlignCenter))
layout.addWidget(subCategory)

layout.addWidget(ISBNEdit)
layout.addWidget(ISBNButton)
# Call lookup when user presses Enter or clicks button
ISBNEdit.returnPressed.connect(lookup)
ISBNButton.clicked.connect(lookup)

# Create the central widget which contains the layout
central_widget = QWidget()
central_widget.setLayout(layout)
# Set the central widget in the main window
window.setCentralWidget(central_widget)
window.setWindowTitle("Categorize Book by ISBN")
window.show()
window.setWindowState(Qt.WindowMaximized)
app.exec_()