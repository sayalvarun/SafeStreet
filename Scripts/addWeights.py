import csv

num = 0
rows = list()
with open('../data/Felonies.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if num == 0:
			rows.append(row)
			num += 1
			continue

		offense = row[4]
		weight = 1
		if offense == "GRAND LARCENY":
			weight = 3
		elif offense == "FELONY ASSAULT":
			weight = 2
		elif offense == "MURDER & NON-NEGL. MANSLAUGHTE":
			weight = 5
		elif offense == "GRAND LARCENY OF MOTOR VEHICLE":
			weight = 2
		elif offense == "ROBBERY":
			weight = 3
		elif offense == "GRAND LARCENY":
			weight = 3
		elif offense == "BURGLARY":
			weight = 1
		elif offense == "RAPE":
			weight = 4

		if len(row) == 12:
			row.append(str(weight))
		else:
			row[12] = str(weight)

		rows.append(row)

		num += 1

#for row in rows:
	#print(str(row))

with open('../data/out.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(rows)