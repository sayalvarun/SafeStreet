#84,112
import math 
import sys
import pickle

startLat = 40.5683282534
startLong = -74.0413284302
endLat = 40.866276056
endLong = -73.7635803223
r_earth = 6378
dy = 0.2955
dx = 0.2802
grid_id = 0
grids = {}
rows = {}
row_id = 0
currLat = startLat
currLong = startLong
new_grid = pickle.load(open("new_grid.pkl","rb"))
new_rows = pickle.load(open("rows.pkl","rb"))

def calculate_grids():
	global grids
	global rows
	while currLat < endLat:
		rows[row_id] = [currLat,grid_id]
		currLong = startLong
		newLat  = currLat  + (dy / r_earth) * (180 / math.pi)
		while currLong < endLong:
			oldLong = currLong
			currLong = currLong + (dx / r_earth) * (180 / math.pi) / math.cos(currLat * math.pi/180);
			grids[grid_id] = {'BL_LAT':currLat,'BL_LONG':oldLong,'TR_LAT':newLat,'TR_LONG':currLong,'ROW_ID':row_id,'SCORE':0}
			grid_id = grid_id + 1
		currLat = newLat
		row_id = row_id + 1
	pickle.dump(grids,open("Grid.pkl","wb"))
	pickle.dump(rows,open("rows.pkl","wb"))


def get_details(grid_num):
	global new_grid
	if grid_num < 0 or grid_num > len(new_grid.keys()):
		print "in get details"
		return -1
	return new_grid[grid_num]

def find_grid(lat,lon):
	global new_grid
	global new_rows
	dict = {}
	finalRow = -1
	for row in range(0,len(new_rows.keys()) - 1):
		if lat <= new_rows[len(new_rows.keys()) - 1][0] and row + 1 < len(new_rows.keys()) and new_rows[row][0] <= lat and new_rows[row+1][0] > lat: 
			finalRow = row
	if finalRow < 0:
		return -1,dict
	else:
		start_grid = new_rows[finalRow][1]
		finalCol = -1
		for col in range(start_grid, start_grid + 85):
			if col < len(new_grid.keys()) and new_grid[col]['BL_LONG'] <= lon and new_grid[col]['TR_LONG'] > lon:
				finalCol = col
	if finalCol == -1:
		return -1,dict
	return finalCol,new_grid[finalCol]

def calc(coords):
	grids = pickle.load(open("Grid.pkl","rb"))
	rows = pickle.load(open("rows.pkl","rb"))
	lists = []
	count = 0
	for coord in coords:
		lat = coord[0]
		lon = coord[1]
		finalRow = -1
		for row in range(0,len(rows.keys()) - 1):
			if lat <= rows[len(rows.keys()) - 1][0] and row + 1 < len(rows.keys()) and rows[row][0] <= lat and rows[row+1][0] > lat: 
				finalRow = row
		if finalRow < 0:
			lists.append(finalRow)
		else:
			start_grid = rows[finalRow][1]
			finalCol = -1
			for col in range(start_grid, start_grid + 85):
				if col < len(grids.keys()) and grids[col]['BL_LONG'] <= lon and grids[col]['TR_LONG'] > lon:
					finalCol = col
			if finalCol == -1:
				count = count + 1
			lists.append(finalCol)
	return lists

if __name__ == "__main__":
	latitude = 0.0
	longitude = 0.0
	if len(sys.argv) >= 2:
		latitude = sys.argv[1]
		longitude = sys.argv[2]
	#calculate_grids()
	print find_grid(float(latitude),float(longitude))

