#84,112
import math 
import sys
import pickle

class squares(object):
	def __init__(self):
		self.startLat = 40.5683282534
		self.startLong = -74.0413284302
		self.endLat = 40.866276056
		self.endLong = -73.7635803223
		self.r_earth = 6378
		self.dy = 0.2955
		self.dx = 0.2802
		self.grid_id = 0
		self.grids = {}
		self.rows = {}
		self.row_id = 0
		self.currLat = self.startLat
		self.currLong = self.startLong

	def calculate_grids(self):
		while self.currLat < self.endLat:
			self.rows[self.row_id] = [self.currLat,self.grid_id]
			self.currLong = self.startLong
			newLat  = self.currLat  + (self.dy / self.r_earth) * (180 / math.pi)
			while self.currLong < self.endLong:
				oldLong = self.currLong
				self.currLong = self.currLong + (self.dx / self.r_earth) * (180 / math.pi) / math.cos(self.currLat * math.pi/180);
				self.grids[self.grid_id] = {'BL_LAT':self.currLat,'BL_LONG':oldLong,'TR_LAT':newLat,'TR_LONG':self.currLong,'ROW_ID':self.row_id,'SCORE':0}
				self.grid_id = self.grid_id + 1
			self.currLat = newLat
			self.row_id = self.row_id + 1
		pickle.dump(self.grids,open("Grid.pkl","wb"))

	def find_grid(self,lat,long):
		finalRow = -1
		for row in range(0,len(self.rows.keys()) - 1):
			if lat <= self.rows[len(self.rows.keys()) - 1][0] and row + 1 < len(self.rows.keys()) and self.rows[row][0] <= lat and self.rows[row+1][0] > lat: 
				finalRow = row
		if finalRow < 0:
			return -1
		start_grid = self.rows[finalRow][1]
		finalCol = -1
		for col in range(start_grid, start_grid + 85):
			if col < len(self.grids.keys()) and self.grids[col]['BL_LONG'] <= long and self.grids[col]['TR_LONG'] > long:
				finalCol = col
		return finalCol

if __name__ == "__main__":
	latitude = 0.0
	longitude = 0.0
	if len(sys.argv) >= 2:
		latitude = sys.argv[1]
		longitude = sys.argv[2]
	sqr = squares()
	sqr.calculate_grids()
	print sqr.find_grid(float(latitude),float(longitude))


