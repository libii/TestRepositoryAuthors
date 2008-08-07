#!/usr/bin/env python

import os, sys

import meshPartitioner.conf.confLoader as confLoader

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-v", "--vals-per-point", dest="vals_per_point", default="", type="string",
			  help="Values per point (default will use configuration file value")

progName = sys.argv[0]
usage = progName + ""
usage = progName + " MESH_FILE DIM1 DIM2 [DIM3]"

parser.set_usage(usage)

(options, args) = parser.parse_args()

conf = confLoader.ConfLoader(options.conf_file)

dataType = conf.getDataType()
if options.vals_per_point:
	valsPerPoint = int(options.vals_per_point)
else:
	valsPerPoint = conf.getValuesPerPoint()

dims = []

if len(args) == 0:
	dims = conf.getInputMeshDimensions()
	meshFile = conf.getInputMesh()
else:
	meshFile = args[0]
	for i in range(1, len(args)):
		dims.append(int(args[i]))
if len(dims) == 2:
	#2D
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D as MeshTools
elif len(dims) == 3:
	# 3D
	from meshPartitioner.mesh3D.meshTools3D import MeshTools3D as MeshTools
else:
	print str(len(dims)) + "D meshes are not supported!"
	parser.print_usage()
	sys.exit(1)

meshFile = os.path.abspath(meshFile)
meshTools = MeshTools(dataType, conf.getInputEndianness(), conf.getOutputEndianness(), valsPerPoint, conf.getValuesToInclude())
print "Mesh: " + meshFile + " " + str(dims) + " (" + str(conf.getValuesPerPoint()) + " Values Per Point)"

mesh = meshTools.loadMesh(meshFile, dims)
meshTools.printMesh(mesh)