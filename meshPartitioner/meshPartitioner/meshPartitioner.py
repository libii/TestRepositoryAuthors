import os, sys, struct, math

import mesh2D.meshTools2D as meshTools2D
import mesh3D.meshTools3D as meshTools3D
from meshToolsAPI import TYPE_FLOAT
from util.pieceUtils import PieceNameGenerator

yifengFileNames = True

class MeshPartitioner:
	
	def __init__(self, meshTools, inputMesh, outputDir, dimensions, pieces, fileNamePattern):
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
		
		fileNameSplit = self.inputMesh.split(os.sep)
		baseFileName = fileNameSplit[len(fileNameSplit)-1]
		
		self.nameGen = PieceNameGenerator(baseFileName, fileNamePattern, self.dimensions, self.pieces, self.pieceWidths)
	
	def partition(self, absStart=None, absEnd=None, startIndices=None, endIndices=None, zyx=False):
		verbose=True
		
		if startIndices:
			for i in range(len(startIndices)):
				index = startIndices[i]
				pieces = self.pieces[i]
				if index >= pieces:
					sys.stderr.write("ERROR: Start partition index out of bounds!\n")
					return
		else:
			startIndices = [0, 0, 0]
		
		if not absStart:
			absStart = 0
		
		if not absEnd:
			absEnd = 1
			for piece in self.pieces:
				absEnd *= piece
		
		if endIndices:
			for i in range(len(endIndices)):
				index = endIndices[i]
				pieces = self.pieces[i]
				if index >= pieces:
					sys.stderr.write("Warning: End partition index out of bounds...set to max.\n")
					endIndices[i] = pieces - 1 
		else:
			endIndices = []
			for piece in self.pieces:
				endIndices.append(piece - 1)
		
		digits = 0
		if yifengFileNames:
			num = 1
			for piece in self.pieces:
				num *= piece
			digits = len(str(piece - 1))
		else:
			for num in self.pieces:
				length = len(str(num))
				if length > digits:
					digits = length
		
		count = int(0)
		absStart = int(absStart)
		absEnd = int(absEnd)
		
		for index1 in range(startIndices[0], endIndices[0]+1):
			coord1 = self.pieceWidths[0] * index1
			for index2 in range(startIndices[1], endIndices[1]+1):
				coord2 = self.pieceWidths[1] * index2
				if self.numDimensions == 3:
					for index3 in range(startIndices[2], endIndices[2]+1):
						
						if absStart > count:
							count += 1
							continue
						if count > absEnd:
							return
						
						coord3 = self.pieceWidths[2] * index3
						indices = []
						indices.append(index1)
						indices.append(index2)
						indices.append(index3)
						startCoords = []
						startCoords.append(coord1)
						startCoords.append(coord2)
						startCoords.append(coord3)
						self._extract(indices, startCoords, digits, verbose, zyx=zyx)
						count += 1
				else:
					
					if absStart > count:
						count += 1
						continue
					if count > absEnd:
						return
					
					indices = []
					indices.append(index1)
					indices.append(index2)
					startCoords = []
					startCoords.append(coord1)
					startCoords.append(coord2)
					self._extract(indices, startCoords, digits, verbose)
					count += 1
	
	def _extract(self, indices, startCoords, digits, verbose=False, zyx=False):
		
		pieceFile = self.outputDir + self.nameGen.getFileName(indices, zyx)
		
		#if yifengFileNames:
		#	pieceFile = self.outputDir + baseFileName.rstrip(".bin")
		#	pieceFile += self.padNum(index, digits) + ".bin"
		#else:
		#	pieceFile = self.outputDir + baseFileName
		#	for index in indices:
		#		pieceFile = pieceFile + "_" + self.padNum(index, digits) 
		
		if verbose:
			printStr = "Index:"
			
			for index in indices:
				printStr = printStr + " " + str(index)
			
			printStr += "=>" + str(self.nameGen.calcIndexes(indices, self.pieceWidths))
			
			printStr = printStr + " Start:"
			
			for coord in startCoords:
				printStr = printStr + " " + str(coord)
			
			printStr = printStr + " End:"
			
			for i in range(len(startCoords)):
				printStr = printStr + " " + str(startCoords[i] + self.pieceWidths[i])
			
			print "Writing piece " + pieceFile + " " + printStr
		
		piece = self.meshTools.extractMeshPeiceFromFile(self.inputMesh, self.dimensions,\
															startCoords, self.pieceWidths, outFile=pieceFile, zyx=zyx)
	
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
						for dim3 in range(0, self.pieceWidths[2]):
							mesh[startCoords[2] + dim3][startCoords[1] + dim2][startCoords[0] + dim1] = piece[dim3][dim2][dim1]
					else:
						mesh[startCoords[1] + dim2][startCoords[0] + dim1] = piece[dim2][dim1]
		
		return mesh
	
if __name__ == "__main__":
	meshFile = "mesh.bin"
	numX = 4
	numY = 4
	numZ = 4
	
	xPieces = 4
	yPieces = 4
	zPieces = 4
	
	meshTools = meshTools3D.MeshTools3D(TYPE_FLOAT, valsPerPoint=5)
	
	dimensions = [numX, numY, numZ]
	pieces = [xPieces, yPieces, zPieces]
	
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