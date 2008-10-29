import struct

try:
	from meshToolsAPI import *
except:
	from meshPartitioner.meshToolsAPI import *

class MeshTools2D(MeshToolsAPI):
	
	def __init__(self, type, inputEndianness="=", outputEndianness="=", valsPerPoint=1, valsToInclude=None):
		MeshToolsAPI.__init__(self, type, inputEndianness, outputEndianness, valsPerPoint, valsToInclude)
	
	def loadMesh(self, meshFile, dimensions):
		"""
		Loads the mesh into a list of lists in the format: y,x
		"""
		numX = dimensions[0]
		numY = dimensions[1]
		file = open(meshFile, "rb")
		
		mesh = []
		for y in range(0, numY):
			yLine = []
			for x in range(0, numX):
				binData = file.read(self.bytesPerPoint)
				point = struct.unpack(self.inUnpackStr, binData)
				if self.valsPerPoint == 1:
					point = point[0]
				yLine.append(point)
			mesh.append(yLine)
		
		file.close()
		
		return mesh
	
	def printMesh(self, mesh, indexesToPrint=None):
		"""
		Prints a string representation of the given mesh
		"""
		
		numY = len(mesh)
		numX = len(mesh[0])
		if not self.checkPrintWarn([numX, numY]):
			return
		
		for xList in reversed(mesh):
			printStr = ""
			for point in xList:
				if len(printStr) > 0:
					printStr = printStr + "\t"
				if indexesToPrint:
					point = self.restructureVals(point, indexesToPrint)
				printStr = printStr + str(point)
			print printStr + "\n"
	
	def writeMesh(self, mesh, fileName):
		fp = open(fileName, "wb")
		
		fmt = self.outputEndianness + self.type
		
		for xList in mesh:
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
		
		widthX = widths[0]
		widthY = widths[1]
		
		mesh = []
		
		# initialize mesh
		for y in range(0, widthY):
			xList = []
			for x in range(0, widthX):
				xList.append(0.0)
			mesh.append(xList)
		
		# copy part
		for y in range(0, widthY):
			for x in range(0, widthX):
				mesh[y][x] =  origMesh[y + startY][x + startX]
		
		return mesh
	
	def extractMeshPeiceFromFile(self, meshFile, dimensions, startCoords, widths, outFile=None, zyx=False):
		"""
		
		"""
		origWidthX = dimensions[0]
		origWidthY = dimensions[1]
		
		startX = startCoords[0]
		startY = startCoords[1]
		
		widthX = widths[0]
		widthY = widths[1]
		
		debug = False
		# this is the number of bytes until the first x per line
		xLineOffset = startX * self.bytesPerPoint
		bytesPerLine = self.bytesPerPoint * origWidthX
		
		if debug:
			print "xLineOffset: " + str(xLineOffset)
			print "bytesPerLine: " + str(bytesPerLine)
		
		file = open(meshFile, "rb")
		
		if outFile:
			out = open(outFile, "wb")
		else:
			mesh = []
		
		index = 0
		
		for y in range(startY, startY + widthY):
			# could optomize here, really only have to do this math once per mesh
			index = bytesPerLine * y
			index += xLineOffset
			
			if debug:
				print "newIndex: " + str(newIndex)
				print "index: " + str(index)
				print "offset: " + str(offset)
			
			file.seek(index)
			
			if not outFile:
				xList = []
			for x in range(widthX):
				binData = file.read(self.bytesPerPoint)
				if outFile and self.valsToInclude == None and self.inputEndianness == self.outputEndianness:
					#print "Writing " + str(point) + " to " + outFile
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
				mesh.append(xList)
		
		if outFile:
			out.close()
			return
		return mesh
	
	def compareMeshes(self, mesh1, mesh2):
		numY = len(mesh1)
		numX = len(mesh1[0])
		
		numY_2 = len(mesh2)
		numX_2 = len(mesh2[0])
		
		if numX != numX_2 or numY != numY_2:
			print "Mesh dimensions don't match!"
			print "Mesh 1: " + str(numX) + " x " + str(numY)
			print "Mesh 2: " + str(numX_2) + " x " + str(numY_2)
			return False
		
		for y in range(0, numY):
			for x in range(0, numX):
				pt1 = mesh1[y][x]
				pt2 = mesh2[y][x]
				
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
		
		fp = open(fileName, "wb")
		
		count = 0
		
		vpp = self.valsPerPoint
		fmt = self.inputEndianness + self.type
		
		for y in range(maxY):
			for x in range(maxX):
				#print str(x) + " " + str(y
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
				for i in range(4, vpp+1):
					if self.isFloatingType():
						vals.append(float(z))
					else:
						vals.append(z)
				
				fp.write(self.packList(fmt, vals))
				
				count += 1
		
		fp.close()