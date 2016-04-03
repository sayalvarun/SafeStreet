import requests
import pprint
import string
import re
import os
import json
import sys
import time
import pickle
import calcGrid

grid = pickle.load(open('new_grid.pkl','rb'))

def getKey():
    f = open('key.txt')
    key = f.read()
    return key

def getWaypoints(points, source, dest):
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='
    url += source
    url += "&destination="
    url += dest
    url += "&mode=walking"
    url += "&waypoints=optimize:true|"
    for point in points:
        url += str(point[0]) + ',' + str(point[1]) + '|'
    url = url[:-1] #remove the extra '|'
    url += "&key="
    url += getKey()
    url = string.replace(url, "\n", "")

    print(url + "\n\n")

    r = requests.get(url)   
    obj = r.json()
    status = obj["status"]
    if status != "OK":
        return None

    return getPolyline(obj)

def getPolyline(obj):
    return obj['routes'][0]['overview_polyline']['points']

def getURL(source, destination):
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='
    url += source
    url += "&destination="
    url += destination
    url += "&mode=walking"
    url += "&key="
    url += getKey()
    return string.replace(url, "\n", "")

def getDirections(source, destination):
    url = getURL(source, destination)
    print(url)
    r = requests.get(url)   
    obj = r.json()
    status = obj["status"]
    if status != "OK":
        return None

    return obj

def getDirectionPoints(source, dest):
	res = getDirections(source, dest)
	locs = []
	start = (res["routes"][0]["legs"][0]["start_location"]["lat"],res["routes"][0]["legs"][0]["start_location"]["lng"])
	locs.append(start)
	#alocs.append(res["routes"][0]["legs"]["end_location"])
	for l in res["routes"][0]["legs"][0]["steps"]:
		locs.append((l["end_location"]["lat"], l["end_location"]["lng"]))
	
	end = (res["routes"][0]["legs"][0]["end_location"]["lat"],res["routes"][0]["legs"][0]["end_location"]["lng"])
	locs.append(end)
	return locs

# Get the tile that is cheapest adjacent neighbor to start
def getCheapestNeighbor(start, up, right, left, down):
	print "cheap :P"
	min = float("inf")
	minindex = start
	if up == 1:
		new = start+84
		new_score = calcGrid.get_details(new)["SCORE"]
		if new_score < min:
			min = new_score
			minindex = new
	if right == 1:
		new = start+1
		new_score = calcGrid.get_details(new)["SCORE"]
		if new_score < min:
			min = new_score
			minindex = new
	if left == 1:
		new = start-1
		new_score = calcGrid.get_details(new)["SCORE"]
		if new_score < min:
			min = new_score
			minindex = new
	if down == 1:
		new = start-1
		new_score = calcGrid.get_details(new)["SCORE"]
		if new_score < min:
			min = new_score
			minindex = new
	print "minindex:",minindex
	return minindex
			
		

def getTilesForLeg(start, end):
	print "get tiles"
	sid = calcGrid.find_grid(start[0],start[1])[0]
	eid = calcGrid.find_grid(end[0],end[1])[0]
	tiles = [calcGrid.get_details(sid)]
	while(eid != sid):
		print "in while"
		retid = sid
		if eid > sid:
			if eid - sid < 84:
				#exclusively right
				retid = getCheapestNeighbor(sid, 0, 1, 0, 0)
				tiles.append(calcGrid.get_details(retid))
			# We can only go up
			elif eid%84 > sid%84:
				# We only go right
				retid = getCheapestNeighbor(sid, 1, 1, 0, 0)
				tiles.append(calcGrid.get_details(retid))
			elif eid%84 < sid%84:
				# We only go left
				retid = getCheapestNeighbor(sid, 1, 0, 1, 0)
				tiles.append(calcGrid.get_details(retid))
			else:
				# exclusively up
				retid = getCheapestNeighbor(sid, 1, 0, 0, 0)
				tiles.append(calcGrid.get_details(retid))
		elif eid < sid:
			# We can only go down
			if sid - eid < 84:
				#exclusively left
				retid = getCheapestNeighbor(sid, 0, 0, 1, 0)
				tiles.append(calcGrid.get_details(retid))
			elif eid%84 > sid%84:
				# and right
				retid = getCheapestNeighbor(sid, 0, 1, 0, 1)
				tiles.append(calcGrid.get_details(retid))
			elif eid%84 < sid%84:
				# And left
				retid = getCheapestNeighbor(sid, 0, 0, 1, 1)
				tiles.append(calcGrid.get_details(retid))
			else:
				#Only down
				retid = getCheapestNeighbor(sid, 0, 0, 0, 1)
				tiles.append(calcGrid.get_details(retid))
		print "sid:",sid
		print "retid:",retid
		print "eid:",eid
		sid = retid
	return tiles

def getMidLatLong(tile):
	x = tile['BL_LAT']
	new_x = x + (tile['TR_LAT'] - x)/2
	y = tile['BL_LONG']
	new_y = y + (tile['TR_LONG'] - y)/2
	return (new_x,new_y)

def computeNewWaypoints(directionList):
	startTup = directionList[0]
	wayps = set()
	for p in directionList[1:-1]:
		tiles = getTilesForLeg(startTup, p)
		pprint.pprint(tiles)
		for t in tiles:
			wayps.add(getMidLatLong(t))
		startTup = p
	return wayps
	

if __name__=="__main__":
	s = "251 Mercer steet, New York NY"
	d = "Empire State Building"
	pprint.pprint(computeNewWaypoints(getDirectionPoints(s,d)))

