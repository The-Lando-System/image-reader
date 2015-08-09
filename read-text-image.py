import argparse
import json
from PIL import Image

parser = argparse.ArgumentParser(description='Provide a path to an image containing text')
parser.add_argument('image', help='Path to the image file')
args = parser.parse_args()

###############
# Convert a set of 2D data into rows
#
# rows = [ row1, row2, ... ]
# row = [ pixel1, pixel2, ...]
# len(rows) = number of entries in a column of pixels
#
##########
def getRowData(data,width):
	rows = []
	row = []

	count = 1

	for i in range(0,len(data)):

		row.append(data[i])

		if (count == width):
			rows.append(row)
			row = []
			count = 0

		count = count + 1

	return rows

###############
#
# cols = [ col1, col2, ... ]
# col = [ pixel1, pixel2, ...]
# len(cols) = number of entries in a row of pixels
#
##########

def getColData(rows):
	cols = []

	for j in range(0,len(rows[0])-1):
		col = []
		for i in range(0,len(rows)-1):
			col.append(rows[i][j])
		cols.append(col)

	return cols


#######
#
# chars = [ char1, char2, char3, ... ]   
# char = [ col1Avg, col2Avg, ... ]
# colAvg = average pixel value of a column
# len(char) = number of columns in a character
# 
####
def getChars(cols):

	chars = []
	char = []

	for i in range(0,len(cols)):

		colTotal = 0
		for j in range(0,len(cols[i])):
			colTotal = colTotal + cols[i][j]

		colAvg = colTotal / len(cols[i])

		if (colAvg < 255):
			char.append(colAvg)
		else:
			chars.append(char)
			char = []


	newChars = []
	for i in range(0,len(chars)):
		if (len(chars[i]) > 1):
			newChars.append(chars[i])
	chars = newChars
	return chars



print("Hello World! Here is my file: " + args.image)

im = Image.open(args.image).convert('L')

print(im.format, im.size, im.mode)

imgWidth, imgHeight = im.size

pixels = list(im.getdata())

rows = getRowData(pixels,imgWidth)
cols = getColData(rows)
chars = getChars(cols)

print("Detected " + str(len(chars)) + "characters")

print("Values for the letter A:")
print(chars[0])

f = open('training_chars.json', 'w')

jsonChars = []
for i in range(0,len(chars)):
	for j in range(0,len(chars[i])):
		jsonChars.append(chars[i][j])
	jsonChars.append(255)
	jsonChars.append(255)

f.write(json.dumps(jsonChars))

f.close()