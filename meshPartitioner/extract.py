#!/usr/bin/env python

import os, sys

import meshPartitioner.conf.confLoader as confLoader
import meshPartitioner.meshPartitioner as meshPartitioner
import meshPartitioner.util.pieceUtils as pieceUtils

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-a", "--absolute-indexes", dest="absolute_indexes", action="store_true", default=False,
			  help="Use absolute indexes instead of partition indexes. For example 0 0 1 would mean point (0, 0, 1) "\
			  + "instead of partition (0, 0, 1). Default uses partition indexes.")
parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-f", "--file", dest="out_file", default="", type="string",
			  help="Output piece to specified file. Default will print a string representation.")

progName = sys.argv[0]
usage = progName + " PARTITION_INDEXES\n"
usage += "\t-- OR --\n"
usage += "\t" + progName + " -a ABSOLUTE_START_INDEXES ABSOLUTE_END_INDEXES\n\n"
usage += "Example: For a 3D mesh, if you wanted to extract partition index [0, 0, 1]\n"
usage += "\t" + progName + " 0 0 1\n\n"
usage += "\tIf you wanted to extract a piece starting at absolute index [0, 0, 1] and ending at absolute index [1, 4, 2]\n"
usage += "\t" + progName + " -a 0 0 1 1 4 2\n"

parser.set_usage(usage)

(options, args) = parser.parse_args()

conf = confLoader.ConfLoader(options.conf_file)

isAbsolute = options.absolute_indexes
outFile = options.out_file

meshFile = conf.getInputMesh()
dims = conf.getInputMeshDimensions()
pieces = conf.getPartitions()

numDims = len(dims)

if numDims == 2:
	# 2D
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D as MeshTools
elif numDims == 3:
	# 3D
	from meshPartitioner.mesh3D.meshTools3D import MeshTools3D as MeshTools

meshTools = MeshTools(conf.getDataType(), conf.getInputEndianness(), conf.getOutputEndianness(), conf.getValuesPerPoint(), conf.getValuesToInclude())

startIndexes = []
widths = []

pieceStr = "Piece "

if isAbsolute:
	endIndexes = []
	if len(args) == (numDims*2):
		
		for i in range(0, numDims):
			startIndexes.append(int(args[i]))
		for i in range(numDims, numDims*2):
			width = int(args[i]) - startIndexes[i - numDims]
			widths.append(width + 1)
	else:
		parser.print_usage()
		sys.exit(1)
else:
	if len(args) == numDims:
		pieceWidths = pieceUtils.loadPieceWidths(dims, pieces)
		
		for i in range(0, numDims):
			pieceStr += " " + args[i]
			start = int(args[i]) * pieceWidths[i]
			startIndexes.append(start)
			widths.append(pieceWidths[i])
		pieceStr += " ==> "
	else:
		parser.print_usage()
		sys.exit(1)

pieceStr += "from:"

for start in startIndexes:
	pieceStr += " " + str(start)

pieceStr += " to:"

for i in range(0, len(startIndexes)):
	start = startIndexes[i]
	width = widths[i]
	pieceStr += " " + str(start + width - 1)

if outFile:
	print "Writing " + pieceStr + " to " + outFile
	meshTools.extractMeshPeiceFromFile(meshFile, dims, startIndexes, widths, outFile=outFile)
else:
	print pieceStr
	mesh = meshTools.extractMeshPeiceFromFile(meshFile, dims, startIndexes, widths)
	meshTools.printMesh(mesh)