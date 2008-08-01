"""
This is a simple test that loads a binary mesh, and saves it to another file.

It then verifies that the files are the same
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
			dims = [numX, numY]
			mesh = self.meshTools.loadMesh(meshFile, dims)
			fileName = meshFile + ".copy"
			self.meshTools.writeMesh(mesh, fileName)
			meshCopy = self.meshTools.loadMesh(fileName, dims)
			os.unlink(fileName)
			if not self.meshTools.compareMeshes(mesh, meshCopy):
				return False
		return True


if __name__ == "__main__":
	from meshPartitioner.mesh2D.meshTools2D import MeshTools2D
	from meshPartitioner.mesh2D.meshTools2D import TYPE_FLOAT
	
	meshTools = MeshTools2D(TYPE_FLOAT, 5)
	
	tester = Test(meshTools)
	tester.test()