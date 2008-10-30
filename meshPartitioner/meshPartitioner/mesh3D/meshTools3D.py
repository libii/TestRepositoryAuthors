import struct, sys

try:
	from meshToolsAPI import *
except:
	from meshPartitioner.meshToolsAPI import *

class MeshTools3D(MeshToolsAPI):
	
	def __init__(self, type, inputEndianness="=", outputEndianness="=", valsPerPoint=1, valsToInclude=None):
		MeshToolsAPI.__init__(self, type, inputEndianness, outputEndianness, valsPerPoint, valsToInclude)
	
	def loadMesh(self, meshFile, dimensions):
		"""
		Loads the mesh into a list of lists in the format: z,y,x
		"""
		numX = dimensions[0]
		numY = dimensions[1]
		numZ = dimensions[2]
		file = open(meshFile, "rb")
		
		mesh = []
		for z in range(0, numZ):
			zLine = []
			for y in range(0, numY):
				yLine = []
				for x in range(0, numX):
					binData = file.read(self.bytesPerPoint)
					#print "LENGTH: " + str(len(binData))
					point = struct.unpack(self.inUnpackStr, binData)
					#print "Read " + str(point) + " from " + meshFile
					if self.valsPerPoint == 1:
						point = point[0]
					yLine.append(point)
				zLine.append(yLine)
			mesh.append(zLine)
		
		file.close()
		
		return mesh
	
	def printMesh(self, mesh, indexesToPrint=None, warn=True):
		"""
		Prints a string representation of the given mesh
		"""
		
		numZ = len(mesh)
		numY = len(mesh[0])
		numX = len(mesh[0][0])
		
		if not self.checkPrintWarn([numX, numY, numZ]):
			return
		
		for y in reversed(range(0, numY)):
			for z in reversed(range(0, numZ)):
				printStr = ""
				for x in range(0, numX):
					if len(printStr) > 0:
						printStr = printStr + "\t"
					point = mesh[z][y][x]
					if indexesToPrint:
						point = self.restructureVals(point, indexesToPrint)
					printStr = printStr + str(point)
				print printStr
			print
	
	def writeMesh(self, mesh, fileName):
		fp = open(fileName, "wb")
		
		fmt = self.outputEndianness + self.type
		
		for yList in mesh:
			for xList in yList:
				for x in xList:
					if self.valsPerPoint == 0:
						binData=struct.pack(fmt, x)
					else:
						binData = ""
						for val in x:
							binData= binData + struct.pack(fmt, val)
					fp.write(binData)
		
		fp.close()
	
	def extractMeshPeiceFromMemory(self, origMesh, startCoords, widths):
		startX = startCoords[0]
		startY = startCoords[1]
		startZ = startCoords[2]
		
		widthX = widths[0]
		widthY = widths[1]
		widthZ = widths[2]
		
		mesh = []
		
		# initialize mesh
		for z in range(0, widthZ):
			yList = []
			for y in range(0, widthY):
				xList = []
				for x in range(0, widthX):
					xList.append(0.0)
				yList.append(xList)
			mesh.append(yList)
		
		# copy part
		for z in range(0, widthZ):
			for y in range(0, widthY):
				for x in range(0, widthX):
					mesh[z][y][x] =  origMesh[z + startZ][y + startY][x + startX]
		
		return mesh
	
	def extractMeshPeiceFromFileZYX(self, meshFile, dimensions, startCoords, widths, outFile=None):
		origWidthX = dimensions[0]
		origWidthY = dimensions[1]
		origWidthZ = dimensions[2]
		
		startX = startCoords[0]
		startY = startCoords[1]
		startZ = startCoords[2]

		pieceWidthX = widths[0]
		pieceWidthY = widths[1]
		pieceWidthZ = widths[2]
		
		# the number of bytes within each small line until the first value
		smallLineOffset = startZ * self.bytesPerPoint
		
		bytesPerSmallLine = origWidthZ * self.bytesPerPoint
		bytesPerMediumLine = origWidthY * bytesPerSmallLine
		
		if outFile == None:
			mesh = []
			for z in range(pieceWidthZ):
				yList = []
				for y in range(pieceWidthY):
					xList = []
					for x in range(pieceWidthX):
						xList.append(None)
					yList.append(xList)
				mesh.append(yList)
		else:
			out = open(outFile, "wb")
		
		file = open(meshFile, "rb")

		for x in range(startX, startX + pieceWidthX):
			for y in range(startY, startY + pieceWidthY):
				# calculate the index of the start of this line
				index = bytesPerSmallLine * x + (bytesPerMediumLine * y) + smallLineOffset
				
				file.seek(index)
				
				for z in range(pieceWidthZ):
					binData = file.read(self.bytesPerPoint)
					if outFile and self.valsToInclude == None and self.inputEndianness == self.outputEndianness:
						# we get to just copy the data
						out.write(binData)
					else:
						# we're restructuring or converting the data
						point = struct.unpack(self.inUnpackStr, binData)
						if self.valsPerPoint == 1:
							point = point[0]
						else:
							point = self.restructureVals(point)
						if outFile:
							binData = self.packList(self.outputEndianness + self.type, point)
							out.write(binData)
						else:
							mesh[z][y][x] = point
		
		file.close()
		
		if outFile != None:
			out.close()
			return
		return mesh
	
	def extractMeshPeiceFromFile(self, meshFile, dimensions, startCoords, widths, outFile=None, zyx=False):
		"""
		
		"""
		if zyx:
			return self.extractMeshPeiceFromFileZYX(meshFile, dimensions, startCoords, widths, outFile)
		origWidthX = dimensions[0]
		origWidthY = dimensions[1]
		origWidthZ = dimensions[2]
		
		startX = startCoords[0]
		startY = startCoords[1]
		startZ = startCoords[2]
		
		widthX = widths[0]
		widthY = widths[1]
		widthZ = widths[2]
		
		debug = False
		# this is the number of bytes until the first y per line
		yLineOffset = startY * self.bytesPerPoint
		# this is the number of bytes until the first x per y section
		xLineOffset = startX * self.bytesPerPoint
		
		bytesPerYLine = self.bytesPerPoint * origWidthX
		bytesPerZLine = origWidthY * bytesPerYLine
		
		
		if debug:
			print "xLineOffset: " + str(xLineOffset)
			print "yLineOffset: " + str(yLineOffset)
			print "bytesPerYLine: " + str(bytesPerYLine)
			print "bytesPerZLine: " + str(bytesPerZLine)
		
		file = open(meshFile, "rb")
		
		if outFile:
			out = open(outFile, "wb")
		else:
			mesh = []
		
		index = 0
		
		for z in range(startZ, startZ + widthZ):
			if not outFile:
				yList = []
			for y in range(startY, startY + widthY):
				
				if debug:
					print "Y: " + str(y) + " Z: " + str(z)
				index = bytesPerZLine * z
				index += (bytesPerYLine * y) + xLineOffset
				
				if debug:
					print "index: " + str(index)
				
				file.seek(index)
				
				if not outFile:
					xList = []
				for x in range(widthX):
					binData = file.read(self.bytesPerPoint)
					if outFile and self.valsToInclude == None and self.inputEndianness == self.outputEndianness:
						# we get to just copy the data
						out.write(binData)
					else:
						point = struct.unpack(self.inUnpackStr, binData)
						if self.valsPerPoint == 1:
							point = point[0]
						else:
							point = self.restructureVals(point)
						if outFile:
							binData = self.packList(self.outputEndianness + self.type, point)
							out.write(binData)
						else:
							xList.append(point)
				if not outFile:
					yList.append(xList)
			if not outFile:
				mesh.append(yList)
		
		file.close()
		
		if outFile:
			out.close()
			return
		return mesh
	
	def compareMeshes(self, mesh1, mesh2):
		numZ = len(mesh1)
		numY = len(mesh1[0])
		numX = len(mesh1[0][0])
		
		numZ_2 = len(mesh2)
		numY_2 = len(mesh2[0])
		numX_2 = len(mesh2[0][0])
		
		if numX != numX_2 or numY != numY_2 or numZ != numZ_2:
			print "Mesh dimensions don't match!"
			print "Mesh 1: " + str(numX) + " x " + str(numY) + " x " + str(numZ)
			print "Mesh 2: " + str(numX_2) + " x " + str(numY_2) + " x " + str(numZ_2)
			return False
		
		for z in range(0, numZ):
			for y in range(0, numY):
				for x in range(0, numX):
					pt1 = mesh1[z][y][x]
					pt2 = mesh2[z][y][x]
					
					if self.valsPerPoint == 1:
						if pt1 != pt2:
							return False
					else:
						for i in range(0, len(pt1)):
							if pt1[i] != pt2[i]:
								return False
		
		return True
	
	def writeTestMesh(self, fileName, widths):
		maxX = widths[0]
		maxY = widths[1]
		maxZ = widths[2]
		
		fp = open(fileName, "wb")
		
		count = 0
		
		points = maxX * maxY * maxZ
		
		if points > 1000000:
			mod = int(points / 100000)
		elif points > 100000:
			mod = int(points / 10000)
		elif points > 10000:
			mod = int(points / 1000)
		elif points > 1000:
			mod = int(points / 100)
		else:
			mod = 1
		
		vpp = self.valsPerPoint
		fmt = self.inputEndianness + self.type
		
		for z in range(maxZ):
			for y in range(maxY):
				for x in range(maxX):
					#if count % mod == 0:
					#	print str(x) + " " + str(y) + " " + str(z)
					vals = []
					if vpp >= 1:
						if self.isFloatingType():
							vals.append(float(count))
						else:
							vals.append(count)
					if vpp >= 2:
						if self.isFloatingType():
							vals.append(float(x))
						else:
							vals.append(x)
					if vpp >= 3:
						if self.isFloatingType():
							vals.append(float(y))
						else:
							vals.append(y)
					if vpp >= 4:
						if self.isFloatingType():
							vals.append(float(z))
						else:
							vals.append(z)
					for i in range(5, vpp+1):
						if self.isFloatingType():
							vals.append(float(z))
						else:
							vals.append(z)
					
					fp.write(self.packList(fmt, vals))
					
					count += 1
					
		fp.close()

if __name__ == "__main__":
	tools = MeshTools3D(TYPE_FLOAT, 5)
	
	meshFile = "mesh.bin"
	dims = [4, 4, 4]
	
	mesh = tools.loadMesh("/home/kevin/workspace_python/meshPartitioner/mesh_4_4_4.bin", dims)
	tools.printMesh(mesh)
	
	sys.exit(0)
	
	mesh = tools.loadMesh(meshFile, dims)
	print "\nORIG\n"
	tools.printMesh(mesh)
	
	startCoords = [0, 0, 0]
	widths = [2,2,2]
	
	pieceFile = "tmp_piece.bin"
	
	filePart = tools.extractMeshPeiceFromFile(meshFile, dims, startCoords, widths, outFile=pieceFile)
	
	piece = tools.loadMesh(pieceFile, widths)
	
	print "\nEXTRACTED TO MEM\n"
	tools.printMesh(filePart)
	
	print "\nEXTRACTED TO FILE\n"
	tools.printMesh(piece)
	if tools.compareMeshes(filePart, piece):
		print "They match!"
	else:
		print "They don't match!!"