"""
This is a simple test that loads a binary mesh and partitions it

It then stitches it back together and verifies that it is the same.
"""

import os

import test

class Test(test.Test):
	
	def __init__(self, meshTools):
		name = "Mesh Load/Save/Compare Test"
		test.Test.__init__(self, meshTools, name)
		
		
	
	def test(self):
		for meshFile in self.mesh_list:
			numX, numY = self.extractSizeFromMeshName(meshFile)
			mesh = self.meshTools.loadMesh(meshFile, numX, numY)
			fileName = meshFile + ".copy"
			self.meshTools.writeMesh(mesh, fileName)
			meshCopy = self.meshTools.loadMesh(fileName, numX, numY)
			os.unlink(fileName)
			if not self.meshTools.compareMeshes(mesh, meshCopy):
				return False
		return True