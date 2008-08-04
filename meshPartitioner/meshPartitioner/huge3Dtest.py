
import os

from meshPartitioner import MeshPartitioner
from mesh3D.meshTools3D import MeshTools3D
from meshToolsAPI import TYPE_FLOAT
import util.fileUtils as fileUtils

partition = False

tools = MeshTools3D(TYPE_FLOAT, 5)

dims = [1000, 1000, 1000]

meshFile = "mesh_" + str(dims[0]) + "_" + str(dims[1]) + "_" + str(dims[2])

if not os.path.exists(meshFile):
	print "Writing " + meshFile
	tools.writeTestMesh(meshFile, dims)

pieces = [2, 2, 1]

meshDir = meshFile + "_PARTS"

if os.path.exists(meshDir):
	fileUtils.rmdir(meshDir, verbose=True)

parter = MeshPartitioner(tools, meshFile, meshDir, dims, pieces)

parter.partition()