#!/usr/bin/env python

import os, sys

import meshPartitioner.conf.confLoader as confLoader
import meshPartitioner.meshPartitioner as meshPartitioner
import meshPartitioner.util.pieceUtils as pieceUtils

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-p", "--print", dest="doPrint", action="store_true", default=False,
			  help="Print a string representation instead of writing to a file")
parser.add_option("-V", "--values", dest="vals", default="", type="string",
			  help="Values to print from each point, comma separated (default will use configuration file values)")
parser.add_option("-v", "--vals-per-point", dest="vpp", default=None, type="int",
			  help="Values per point (default will use configuration file value")

progName = sys.argv[0]
usage = progName + " OUT_FILE_NAME\n"
usage += "\t-- OR --\n"
usage += "\t" + progName + " -p/--print\n"
usage += "\t-- OR --\n"
usage += "\t" + progName + " IN_FILE_NAME DIM1 DIM2 [DIM3] OUT_FILE_NAME\n"
usage += "\t-- OR --\n"
usage += "\t" + progName + " -p/--print IN_FILE_NAME DIM1 DIM2 [DIM3]"

parser.set_usage(usage)

(options, args) = parser.parse_args()

doPrint = options.doPrint

numArgs = len(args)

def fail(parser):
	parser.print_usage()
	sys.exit(1)

conf = confLoader.ConfLoader(options.conf_file)

if options.vpp != None:
	vpp = options.vpp
else:
	vpp = conf.getValuesPerPoint()

if vpp <= 1:
	sys.stderr.write("ERROR: Cannot extract values with values per point <= 1" + "\n")
	fail(parser)

if len(options.vals) > 0:
	vals = conf.getValuesToInclude(options.vals)
else:
	vals = conf.getValuesToInclude()

try:
	if len(vals) == 0:
		sys.stderr.write("ERROR: 0 values to extract!" + "\n")
		fail(parser)
except:
	sys.stderr.write("ERROR parsing values to print. Values should be comma separated, like '1,4,2'" + "\n")
	fail(parser)

if (doPrint and numArgs == 0) or (not doPrint and numArgs == 1):
	# this is an extract using the conf file's mesh
	meshFile = conf.getInputMesh()
	dims = conf.getInputMeshDimensions()
	if doPrint:
		outFile = None
	else:
		outFile = args[0]
else:
	if doPrint:
		if numArgs < 3 or numArgs > 4:
			fail(parser)
		threeDims = numArgs == 4
		outFile = None
	else:
		if numArgs < 4 or numArgs > 5:
			fail(parser)
		threeDims = numArgs == 5
		if threeDims:
			outFile = args[4]
		else:
			outFile = args[3]
	meshFile = args[0]
	x = int(args[1])
	y = int(args[2])
	if threeDims:
		z = int(args[3])
		dims = [x,y,z]
	else:
		dims = [x,y]

numDims = len(dims)

if numDims == 2:
	# 2D
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D as MeshTools
elif numDims == 3:
	# 3D
	from meshPartitioner.mesh3D.meshTools3D import MeshTools3D as MeshTools

meshTools = MeshTools(conf.getDataType(), conf.getInputEndianness(), conf.getOutputEndianness(), vpp, vals)

meshTools.extractVals(meshFile, dims, outFile)