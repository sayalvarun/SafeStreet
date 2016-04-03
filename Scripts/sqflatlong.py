import sys
import latlong

ADDR_NUM_COL = 12
ST_NAME_COL = 13
ST_INTER_COL = 14
ST_CROSS_COL = 15

output = open("output.txt","w")

with open("../Data/reducedSqf.csv") as f:
	count = 0
	for line in f:
		if count == 0:
			count+=1
			continue
		row = line.split(",")
		addrnum = row[ADDR_NUM_COL].strip()
		stname = row[ST_NAME_COL].strip()
		interst = row[ST_INTER_COL].strip()
		crossst = row[ST_CROSS_COL].strip()
		
		if addrnum != "" and stname != "":
			q = addrnum+" "+stname+", new york, NY"
			lat, lng = latlong.getLatLong(addrnum+" "+stname+", new york, NY")
		else:
			q = interst+" and "+crossst+", new york, NY"
			lat, lng = latlong.getLatLong(interst+" and "+crossst+", new york, NY")
		
		count+=1
		
		outline = str(lat)+","+str(lng)+"\n"
		output.write(outline)



