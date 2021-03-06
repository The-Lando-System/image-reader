import argparse
import json
from PIL import Image

##################################################################
#                          Methods
##################################################################

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

	for j in range(0,len(rows[0])):
		col = []
		for i in range(0,len(rows)):
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


#############
#
# trainedChars = { 'A' : char[0] , 'B' : char[1] }
#
#######
def trainChars(imageChars,textChars):

	trainedChars = {}

	for i in range(0,len(imageChars)):
		trainedChars[textChars[i]] = imageChars[i]

	return trainedChars

#################
#
# parse the image for characters
#
########
def parseImage(imageFile):

	print("Reading image : " + imageFile)

	im = Image.open(imageFile).convert('L')
	print("-----------------")
	print("-- Image stats --")
	print("-----------------")
	print(im.format, im.size, im.mode)
	print("-----------------")

	imgWidth, imgHeight = im.size

	pixels = list(im.getdata())

	rows = getRowData(pixels,imgWidth)
	cols = getColData(rows)
	chars = getChars(cols)

	print("Detected " + str(len(chars)) + " characters!\n")

	return chars

#################
#
# dump characters to json
#
########
def dumpCharsToJSON(filename,chars):
	f = open(filename, 'w')
	jsonChars = []
	for i in range(0,len(chars)):
		for j in range(0,len(chars[i])):
			jsonChars.append(chars[i][j])
		jsonChars.append(255)
		jsonChars.append(255)

	f.write(json.dumps(jsonChars))
	f.close()

#####################
#
# Score the test data with the trained data set
#
# scoreTable = { 'H' : scores, 'e' : scores }
# scores = [ score1 (char A), score2, score3, ..., score66]
#
##############
def scoreData(testChars,trainedChars):


	charString = ''

	
	for i in range(0,len(testChars)):

		minVal = 100000
		matchedChar = ''

		for key, value in trainedChars.items():

			penalty = 0

			if (len(testChars[i]) < len(value)):
				charLength = len(testChars[i])
			else:
				charLength = len(value)

			if (len(testChars[i]) == len(value)):
				penalty = 0
			else:
				penalty = 100

			score = 0
			totalDiff = 0

			for k in range(0,charLength):
				
				if (k > 0):

					testDiff = abs( testChars[i][k] - testChars[i][k-1] )
					trainDiff = abs( value[k] - value[k-1] )

					totalDiff = totalDiff + abs(testDiff - trainDiff)


			score = ( totalDiff / (charLength-1) ) + penalty 

			if (score < minVal):
				minVal = score
				matchedChar = key

		print("Best score was the letter: " + matchedChar)
		print("With a score of: " + str(minVal))


		charString = charString + matchedChar

	print("Detected the following string: ")
	print(charString)
	


##################################################################
#                          Main
##################################################################

parser = argparse.ArgumentParser(description='Provide a path to an image containing text')
parser.add_argument('trainImage', help='Path to the training image file')
parser.add_argument('testImage', help='Path to the test image file')
args = parser.parse_args()

print("Parsing the training image...")
trainingChars = parseImage(args.trainImage)
dumpCharsToJSON('training-chars.json',trainingChars)

print("Associating characters to training image...")
f = open('./training-data/char-associations.txt', 'r')
associatedChars = list(f.read())
f.close()
print("Number of chars to associate: " + str(len(associatedChars)) + "\n")

trainedChars = trainChars(trainingChars,associatedChars)

print("Parsing the test image...")
testChars = parseImage(args.testImage)
dumpCharsToJSON('test-chars.json',testChars)

scoreData(testChars,trainedChars)