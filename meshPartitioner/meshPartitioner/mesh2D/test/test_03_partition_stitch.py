"""
This is a simple test that loads a binary mesh and partitions it

It then stitches it back together and verifies that it is the same.
"""

import os, random

import test

from meshPartitioner.meshPartitioner import MeshPartitioner
import meshPartitioner.util.fileUtils as fileUtils

class Test(test.Test):
	
	def __init__(self, meshTools, verbose=False):
		name = "Mesh Partition/Stitch/Compare Test"
		test.Test.__init__(self, meshTools, name, verbose)
	
	def testMesh(self, meshFile, meshDir):
		numX, numY = self.extractSizeFromMeshName(meshFile)
		
		dims = [numX, numY]
		piecesX = -1
		piecesY = -1
		while piecesX <= 0 or numX % piecesX != 0:
			piecesX = random.randint(1, numX)
		
		if piecesX == 1:
			randMin = 2
		else:
			randMin = 1
		
		while piecesY <= 0 or numY % piecesY != 0:
			piecesY = random.randint(randMin, numY)
		
		pieces = [piecesX, piecesY]
		
		if self.verbose:
			print "Partitioning a " + str(numX) + "x" + str(numY) + " mesh into " + str(piecesX) + "x" + str(piecesY) + " pieces"
		
		parter = MeshPartitioner(meshTools, meshFile, meshDir, dims, pieces)
		
		if self.verbose:
			print "Partitioning " + meshFile
		parter.partition()
		
		if self.verbose:
			print "Loading Original " + meshFile
		orig = self.meshTools.loadMesh(meshFile, dims)
		
		if self.verbose:
			print "Stitching " + meshDir
		stitched = parter.stitch()
		
		if self.verbose:
			print "Deleting " + meshDir
		fileUtils.rmdir(meshDir, self.verbose)
		
		if self.verbose:
			print "Comparing original to partition/stitched"
		if not self.meshTools.compareMeshes(orig, stitched):
			if self.verbose:
				print "ERROR: Partition/stitched mesh doesn't match original!"
			return False
		if self.verbose:
			print "Success! Partition/stitched mesh matches original!"
		return True
	
	def test(self):
		meshDir = "test_partition"
		
		if os.path.exists(meshDir):
			fileUtils.rmdir(meshDir, self.verbose)
		
		random.seed()
		for meshFile in self.mesh_list:
			if not self.testMesh(meshFile, meshDir):
				return False
		return True


if __name__ == "__main__":
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D
	from meshPartitioner.mesh2D.meshTools2D import TYPE_FLOAT
	
	meshTools = MeshTools2D(TYPE_FLOAT, 5)
	
	runAll = True
	tester = Test(meshTools, True)
	if runAll:
		tester.test()
	else:
		meshDir = "ind_test"
		meshFile = "mesh_100_300.bin"
		if os.path.exists(meshDir):
			fileUtils.rmdir(meshDir, True)
		tester.testMesh(meshFile, meshDir)