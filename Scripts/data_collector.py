import csv

def getData():

	data = []

	with open('../data/Felonies.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			data.append((row[3],row[12]))


	with open('../data/reducedSqf.csv', 'rU') as f:
		reader = csv.reader(f)
		for row in reader:
			data.append(("("+row[13]+","+row[14]+")",row[15]))

	return data
