import os, struct

import mesh2D.meshTools2D as meshTools2D

class MeshPartitioner:
	
	def __init__(self, meshTools, inputMesh, outputDir, dimensions, pieces):
		"""
		"""
		self.meshTools = meshTools
		self.inputMesh = inputMesh
		self.outputDir = outputDir
		self.dimensions = dimensions
		self.pieces = pieces
		
		self.numDimensions = len(pieces)
		
		if len(pieces) != len(dimensions):
			raise meshTools2D.MeshException("You must specify the number of pieces for each dimension!")
		
		if self.numDimensions == 2:
			print "Partitioning 2D Mesh"
		elif self.numDimensions == 3:
			print "Partitioning 3D Mesh"
		else:
			raise meshTools2D.MeshException("Cannot partition a mesh of " + str(self.numDimensions) + " dimensions")
		
		self.pieceWidths = []
		all_ones = True;
		for i in range(0, len(pieces)):
			width = dimensions[i]
			numPieces = pieces[i]
			
			if width % numPieces != 0 or numPieces > width:
				raise meshTools2D.MeshException("Width of dimension " + str(i+1) + ": " + str(width)\
											+ " cannot be evenly divided into " + str(numPieces) + ".")
			
			if numPieces > 1:
				all_ones = False
			
			self.pieceWidths.append(width / numPieces)
		
		if all_ones:
			raise meshTools2D.MeshException("Nothing to be done!")
		
		# make sure the input mesh exists
		if not os.path.exists(inputMesh):
			raise meshTools2D.MeshException("Mesh file doesn't exist!")
		
		if not os.path.exists(outputDir):
			os.mkdir(outputDir)
		
		if not outputDir.endswith(os.sep):
			self.outputDir = self.outputDir + os.sep
	
	def padNum(self, num, digits):
		numStr = str(num)
		
		while len(numStr) < digits:
			numStr = "0" + numStr
		
		return numStr
	
	def partition(self):
		fileNameSplit = self.inputMesh.split(os.sep)
		baseFileName = fileNameSplit[len(fileNameSplit)-1]
		
		digits = 0
		for num in self.pieces:
			length = len(str(num))
			if length > digits:
				digits = length
		
		for index1 in range(0, self.pieces[0]):
			coord1 = self.pieceWidths[0] * index1
			for index2 in range(0, self.pieces[1]):
				coord2 = self.pieceWidths[1] * index2
				if self.numDimensions == 3:
					for index3 in range(0, self.pieces[2]):
						coord3 = self.pieceWidths[2] * index3
						indices = []
						indices.append(index1)
						indices.append(index2)
						indices.append(index3)
						startCoords = []
						startCoords.append(coord1)
						startCoords.append(coord2)
						startCoords.append(coord3)
						self._extract(baseFileName, indices, startCoords, digits)
				else:
					indices = []
					indices.append(index1)
					indices.append(index2)
					startCoords = []
					startCoords.append(coord1)
					startCoords.append(coord2)
					self._extract(baseFileName, indices, startCoords, digits)
	
	def _extract(self, baseFileName, indices, startCoords, digits):
		verbose = False
		
		piece = self.meshTools.extractMeshPeiceFromFile(self.inputMesh, self.dimensions,\
															startCoords, self.pieceWidths)
		
		pieceFile = self.outputDir + baseFileName
		for index in indices:
			pieceFile = pieceFile + "_" + self.padNum(index, digits) 
		
		print "Writing piece " + pieceFile
		
		if verbose:
			printStr = "Piece"
			
			for index in indices:
				printStr = printStr + " " + str(index)
			
			printStr = printStr + " =>"
			
			for coord in startCoords:
				printStr = printStr + " " + str(coord)
			
			print printStr
			self.meshTools.printMesh(piece)
		
		self.meshTools.writeMesh(piece, pieceFile)
	
	def is3D(self):
		if self.numDimensions == 3:
			return True
	
	def stitch(self):
		fileList = os.listdir(self.outputDir)
		
		mesh = []
		
		# initialize mesh
		for dim1 in range(0, self.dimensions[self.numDimensions - 1]):
			dim2s = []
			for dim2 in range(0, self.dimensions[self.numDimensions - 2]):
				if self.is3D():
					dim3s = []
					for dim3 in range(0, self.dimensions[self.numDimensions - 3]):
						dim3s.append(0.0)
					dim2s.append(dim3s)
				else:
					dim2s.append(0.0)
			mesh.append(dim2s)
		
		for file in fileList:
			file = self.outputDir + file
			if not os.path.isfile(file):
				continue
			fileSplit = file.split("_")
			indices = []
			startCoords = []
			
			for i in range(0, self.numDimensions):
				index = int(fileSplit[len(fileSplit) - (i+1)])
				indices.append(index)
			
			# reverse it because we read it in backwards from the end
			indices.reverse()
			
			for i in range(0, len(indices)):
				startCoords.append(indices[i] * self.pieceWidths[i])
			
			printStr = "loading piece " + file + " at"
			
			for index in indices:
				printStr = printStr + " " + str(index)
			
			printStr = printStr + " =>"
			
			for coord in startCoords:
				printStr = printStr + " " + str(coord)
			
			print printStr
			
			piece = self.meshTools.loadMesh(file, self.pieceWidths)
			
			for dim1 in range(0, self.pieceWidths[0]):
				for dim2 in range(0, self.pieceWidths[1]):
					if self.is3D():
						for dim3 in range(0, self.dimensions[2]):
							mesh[startCoords[2] + dim3][startCoords[1] + dim2][startCoords[0] + dim1] = piece[dim3][dim2][dim1]
					else:
						mesh[startCoords[1] + dim2][startCoords[0] + dim1] = piece[dim2][dim1]
		
		return mesh
	
if __name__ == "__main__":
	meshFile = "mesh.bin"
	numX = 4
	numY = 4
	
	xPieces = 2
	yPieces = 2
	
	meshTools = meshTools2D.MeshTools2D(meshTools2D.TYPE_FLOAT, valsPerPoint=5)
	
	dimensions = [numX, numY]
	pieces = [xPieces, yPieces]
	
	parter = MeshPartitioner(meshTools, "mesh.bin", "partition", dimensions, pieces)
	
	parter.partition()
	orig = meshTools.loadMesh(meshFile, dimensions)
	stitched = parter.stitch()
	
	if meshTools.compareMeshes(orig, stitched):
		print "They match!"
	else:
		print "No joy..."
		#print "ORIG!"
		#meshTools.printMesh(orig)
		#print "STITCHED!"
		#meshTools.printMesh(stitched)