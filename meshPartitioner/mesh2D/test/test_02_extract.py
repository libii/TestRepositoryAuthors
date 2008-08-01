"""
This is a simple test that loads a binary mesh, does a file extraction, and compares it to a memory extraction
"""

import os, random

import test

class Test(test.Test):
	
	def __init__(self, meshTools, verbose=False):
		name = "Mesh Extract Test"
		test.Test.__init__(self, meshTools, name, verbose)
	
	def extractTest(self, meshFile):
		numX, numY = self.extractSizeFromMeshName(meshFile)
		dims = [numX, numY]
		
		# case 1: do  a square extraction
		smallSide = numX
		if numY < smallSide:
			smallSide = numY
		width = random.randint(1, smallSide-1)
		
		if self.verbose:
			print "Loading " + meshFile
		mesh = self.meshTools.loadMesh(meshFile, dims)
		if self.verbose:
			print "Extracting Piece From Memory"
		memMesh = self.meshTools.extractMeshPeiceFromMemory(mesh, [0,0], [width, width])
		if self.verbose:
			print "Extracting Piece From File"
		memMesh = self.meshTools.extractMeshPeiceFromMemory(mesh, [0,0], [width, width])
	
	def test(self):
		random.seed()
		for meshFile in self.mesh_list:
			self.extractTest(meshFile)
			if self.verbose:
				print "Loading " + meshFile
			mesh = self.meshTools.loadMesh(meshFile, dims)
			if self.verbose:
				print "Extracting Piece From Memory "
			if not self.meshTools.compareMeshes(mesh, meshCopy):
				if self.verbose:
					print "ERROR: Copied mesh doesn't match original!"
				return False
			if self.verbose:
				print "Success! Copied mesh matches original!"
		return True


if __name__ == "__main__":
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D
	from meshPartitioner.mesh2D.meshTools2D import TYPE_FLOAT
	
	meshTools = MeshTools2D(TYPE_FLOAT, 5)
	
	tester = Test(meshTools, True)
	tester.test()