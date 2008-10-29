#!/usr/bin/env python

import os, sys, math

import meshPartitioner.conf.confLoader as confLoader

from optparse import OptionParser

path = os.path.abspath(os.path.dirname(sys.argv[0]))
if not path.endswith(os.sep):
	path = path + os.sep

parser = OptionParser()

parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-d", "--output-dir", dest="output_dir", default=".", type="string",
			  help="Output Dir (default = %default)")
parser.add_option("-z", "--fast-zyx", dest="fast_zyx", action="store_true", default=False,
			  help="Mesh is fast Z-Y-X, partition accordingly (default is fast X-Y-Z)")

progName = sys.argv[0]
usage = progName + ""
usage = progName + " NUM_JOBS WALL_TIME_MINUTES"

parser.set_usage(usage)

(options, args) = parser.parse_args()

outputDir = options.output_dir
if not outputDir.endswith(os.sep):
	outputDir += os.sep

if not os.path.exists(outputDir):
	os.mkdir(outputDir)

conf = confLoader.ConfLoader(options.conf_file)

if len(args) != 2:
	parser.print_usage()
	sys.exit(1)

numJobs = int(args[0])

if numJobs <= 0:
	print "The number of jobs must be a positive integer!"
	parser.print_usage()
	sys.exit(1)

wallTimeMinsTotal = int(args[1])

if numJobs < 1:
	print "The wall time must be a integer >= 1"
	parser.print_usage()
	sys.exit(1)

wallTimeHours = int(wallTimeMinsTotal / 60)
wallTimeMins = wallTimeMinsTotal % 60

def padNum(num, digits):
	numStr = str(num)
	while len(numStr) < digits:
		numStr = "0" + numStr
	return numStr

minsStr = padNum(wallTimeMins, 2)

hoursStr = padNum(wallTimeHours, 2)

wallTime = hoursStr + ":" + minsStr + ":00"

digits = len(str(numJobs))

dims = conf.getInputMeshDimensions()
pieces = conf.getPartitions()

numPieces = 1

for piece in pieces:
	numPieces *= piece

print "Making jobs for " + str(numPieces) + " pieces"

if numJobs > numPieces:
	print "ERROR: There are more jobs than pieces! (" + str(numJobs) + " jobs, " + str(numPieces) + " pieces)"
	sys.exit(1)

def writeFile(count, digits, confFile, outputDir, startIndex, endIndex, zyx=False):
	name = outputDir + "partition_" + padNum(count, digits)
	fp = open(name + ".qsub", "w")
	fp.write("#!/bin/bash" + "\n")
	fp.write("#" + "\n")
	fp.write("#PBS -l walltime=" + wallTime + "\n")
	fp.write("#PBS -o " + name + ".out" + "\n")
	fp.write("#PBS -e " + name + ".err" + "\n")
	fp.write("\n")
	zyxStr = ""
	if zyx:
		zyxStr = "--fast-zyx "
	partCommand = path + "partition.py " + zyxStr + "-c " + confFile + " -a " + str(startIndex) + " " + str(endIndex)
	print partCommand
	fp.write(partCommand + "\n")
	fp.close()

piecesPerJob = int(math.ceil(float(numPieces) / float(numJobs)))
print str(piecesPerJob) + " pieces per job"
for i in range(0, numJobs):
	startIndex = i * piecesPerJob
	endIndex = startIndex + piecesPerJob - 1
	
	writeFile(i, digits, conf.getConfFileName(), outputDir, startIndex, endIndex, zyx=options.fast_zyx)