#!/usr/bin/env python

import os, sys

import meshPartitioner.conf.confLoader as confLoader

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-c", "--conf", dest="conf_file", default=confLoader.DEFAULT_CONF_FILE_NAME, type="string",
			  help="Configuration File (default = %default)")
parser.add_option("-a", "--auto-name", dest="auto_name", action="store_true", default=False,
			  help="Auto name the mesh file: mesh_dim1_dim2[_dim3].bin. Default requires a name")

progName = sys.argv[0]
usage = progName + " MESH_FILE DIM1 DIM2 [DIM3]\n"
usage += "\t-- OR --\n"
usage += "\t" + progName + " -a DIM1 DIM2 [DIM3]"

parser.set_usage(usage)

(options, args) = parser.parse_args()

conf = confLoader.ConfLoader(options.conf_file)

autoName = options.auto_name
dataType = conf.getDataType()
valsPerPoint = conf.getValuesPerPoint()

dims = []

if len(args) < 1 and not autoName:
	print "You must specify a filename for the mesh or use Auto-Naming!"
	parser.print_usage()
	sys.exit(1)
else:
	if autoName:
		start = 0
	else:
		meshFile = args[0]
		start = 1
	for i in range(start, len(args)):
		dims.append(int(args[i]))
	if autoName:
		meshFile = "mesh"
		for dim in dims:
			meshFile += "_" + str(dim)
		meshFile += ".bin"
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
meshTools = MeshTools(dataType, conf.getInputEndianness(), conf.getOutputEndianness(), conf.getValuesPerPoint(), conf.getValuesToInclude())
print "Generationg Mesh: " + meshFile + " " + str(dims) + " (" + str(conf.getValuesPerPoint()) + " Values Per Point)"

meshTools.writeTestMesh(meshFile, dims)