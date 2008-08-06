#!/usr/bin/env python

import os, sys, time, math

verbose = True

if len(sys.argv) == 2:
	dir = os.path.abspath(sys.argv[1])
else:
	dir = os.path.abspath(".")

dir += os.sep

dirList = os.listdir(dir)

timeFormat = "%a %b %d %H:%M:%S %Z %Y"

startStr = "End PBS Prologue"
endStr = "Begin PBS Epilogue"
pieceStr = "Writing piece"

def padNum(num, digits):
	if num < 10:
		numStr = "0" + str(num)
	else:
		numStr = str(num)
	while len(numStr) < digits:
		numStr = "0" + numStr
	return numStr

def getTimeStrs(secs):
	secStr = padNum(secs % 60, 2)
	mins = int(math.floor(secs / 60))
	minStr = padNum(mins % 60, 2)
	hours = int(math.floor(mins / 60))
	hourStr = padNum(hours, 2)
	
	return [hourStr, minStr, secStr]

def getTime(secs):
	tuple = getTimeStrs(secs)
	return str(tuple[0]) + ":" + str(tuple[1]) + ":" + str(tuple[2])

jobs = 0
totalSecs = 0
totalPieces = 0

firstStartTime = 3000000000
lastEndTime = 0

for fileName in dirList:
	file = dir + fileName
	
	if os.path.isdir(file):
		continue
	if not file.endswith(".out"):
		continue
	
	fp = open(file, "r")
	
	lines = fp.readlines()
	
	startTime = None
	endTime = None
	pieces = 0
	
	for line in lines:
		if line.startswith(startStr):
			line = line.replace(startStr, "")
			timeStr = line.strip()
			struct_time = time.strptime(timeStr, timeFormat)
			startTime = time.mktime(struct_time)
		elif line.startswith(endStr):
			line = line.replace(endStr, "")
			timeStr = line.strip()
			struct_time = time.strptime(timeStr, timeFormat)
			endTime = time.mktime(struct_time)
		elif line.startswith(pieceStr):
			pieces += 1
	
	if startTime and endTime:
		if endTime > lastEndTime:
			lastEndTime = endTime
		if startTime < firstStartTime:
			firstStartTime = startTime
		seconds = endTime - startTime
		if verbose:
			print "Job " + str(jobs) + ": pieces: " + str(pieces) + " time: " + getTime(seconds)
		jobs += 1
		totalSecs += seconds
		totalPieces += pieces
	else:
		print "WARNING: No time detected!"

if jobs == 0:
	print "ERROR: No output files parsed!"
else:
	print "Total Time: " + getTime(totalSecs)
	print "Total Pieces: " + str(totalPieces)
	secsPerPiece = float(totalSecs) / float(totalPieces)
	print "Average Piece Time: " + getTime(secsPerPiece)
	secsPerJob = float(totalSecs) / float(jobs)
	print "Average Job Time: " + getTime(secsPerJob)
	print
	actualSecs = lastEndTime - firstStartTime
	actualMins = actualSecs / 60
	actualHours = actualMins / 60
	print "Actual Time: " + getTime(actualSecs)
	piecesPerHour = float(totalPieces) / actualHours
	print "Actual Piecs Per Hour: " + str(piecesPerHour)