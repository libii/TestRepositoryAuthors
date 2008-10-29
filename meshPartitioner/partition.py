#!/usr/bin/env python

import os, sys

import meshPartitioner.conf.confLoader as confLoader
import meshPartitioner.meshPartitioner as meshPartitioner

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-a", "--absolute-indexes", dest="abs_indexes", action="store_true", default=False,
			  help="Flag to switch use absolute partition indexes for start/end specification. " + \
			  "Default uses  dimension indexes. See examples")
parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-z", "--fast-zyx", dest="fast_zyx", action="store_true", default=False,
			  help="Mesh is fast Z-Y-X, partition accordingly (default is fast X-Y-Z)")

progName = sys.argv[0]
usage = progName + "a [START_INDEX [END_INDEX]]\n\n"
usage = progName + " [START_INDEXES [END_INDEXES]]\n\n"
usage = usage + "Example: For a 3D mesh, if you wanted to partition starting at index [0, 0, 1]\n"
usage = usage + "\t" + progName + " 0 0 1\n\n"
usage = usage + "\tIf you wanted to partition starting at index [0, 0, 1] and ending at index [1, 4, 2]\n"
usage = usage + "\t" + progName + " 0 0 1 1 4 2\n\n"
usage = usage + "\tIf you wanted to do the 3rd through 6th partitions\n"
usage = usage + "\t" + progName + " -a 2 5\n\n"
usage = usage + "Example: For a 2D mesh, if you wanted to partition starting at index [0, 1]\n"
usage = usage + "\t" + progName + " 0 1\n\n"
usage = usage + "\tIf you wanted to partition starting at index [0, 1] and ending at index [1, 4]\n"
usage = usage + "\t" + progName + " 0 1 1 4"

parser.set_usage(usage)

(options, args) = parser.parse_args()

conf = confLoader.ConfLoader(options.conf_file)

meshFile = conf.getInputMesh()
dims = conf.getInputMeshDimensions()
pieces = conf.getPartitions()
abs_indexes = options.abs_indexes

outputDir = conf.getOutputDir()
if not outputDir:
	fileSplit = meshFile.split(os.sep)
	outputDir = fileSplit[len(fileSplit) - 1]
	for piece in pieces:
		outputDir = outputDir + "_" + str(piece)

outputDir = os.path.abspath(outputDir)

print "outputDir: " + outputDir

numDims = len(dims)

if numDims == 2:
	# 2D
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D as MeshTools
elif numDims == 3:
	# 3D
	from meshPartitioner.mesh3D.meshTools3D import MeshTools3D as MeshTools

meshTools = MeshTools(conf.getDataType(), conf.getInputEndianness(), conf.getOutputEndianness(), conf.getValuesPerPoint(), conf.getValuesToInclude())

partitioner = meshPartitioner.MeshPartitioner(meshTools, meshFile, outputDir, dims, pieces, conf.getFileNamePattern())

startIndexes = None
endIndexes = None
absStart = None
absEnd = None

if abs_indexes:
	if len(args) == 1:
		absStart = int(args[0])
	elif len(args) == 2:
		absStart = int(args[0])
		absEnd = str(args[1])
	else:
		parser.print_usage()
		sys.exit(1)
else:
	if len(args) == numDims or len(args) == (numDims*2):
		startIndexes = []
		for i in range(0, numDims):
			startIndexes.append(int(args[i]))
		
		print "Start Indexes: " + str(startIndexes)
		
		if len(args) == (numDims*2):
			endIndexes = []
			for i in range(numDims, numDims*2):
				endIndexes.append(int(args[i]))
			print "End Indexes: " + str(endIndexes)
		elif len(args) != 0:
			parser.print_usage()
			sys.exit(1)

partitioner.partition(absStart, absEnd, startIndexes, endIndexes, zyx=options.fast_zyx)