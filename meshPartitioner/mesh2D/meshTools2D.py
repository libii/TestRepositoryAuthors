import struct

try:
	from meshToolsAPI import *
except:
	from meshPartitioner.meshToolsAPI import *

class MeshTools2D(MeshToolsAPI):
	
	def __init__(self, type, valsPerPoint=1):
		MeshToolsAPI.__init__(self, type, valsPerPoint)
	
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
				point = struct.unpack(self.unpackStr, binData)
				if self.valsPerPoint == 1:
					point = point[0]
				yLine.append(point)
			mesh.append(yLine)
		
		file.close()
		
		return mesh
	
	def printMesh(self, mesh, indexToPrint=None):
		"""
		Prints a string representation of the given mesh
		"""
		for xList in reversed(mesh):
			printStr = ""
			for x in xList:
				if len(printStr) > 0:
					printStr = printStr + "\t"
				if indexToPrint:
					printStr = printStr + str(x[indexToPrint])
				else:
					printStr = printStr + str(x)
			print printStr + "\n"
	
	def writeMesh(self, mesh, fileName):
		fp = open(fileName, "wb")
		
		for xList in mesh:
			for x in xList:
				if self.valsPerPoint == 0:
					binData=struct.pack("f", x)
				else:
					binData = ""
					for val in x:
						binData= binData + struct.pack("f", val)
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
	
	def extractMeshPeiceFromFile(self, meshFile, dimensions, startCoords, widths):
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
			
			xList = []
			for x in range(widthX):
				binData = file.read(self.bytesPerPoint)
				point = struct.unpack(self.unpackStr, binData)
				if self.valsPerPoint == 1:
					point = point[0]
				xList.append(point)
			mesh.append(xList)
		
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
		
		for y in range(maxY):
			for x in range(maxX):
				print str(x) + " " + str(y)
				vp = float(count)
				vs = float(x)
				th = float(y)
				qp= float(0)
				qps= float(0)
				
				binData=struct.pack("fffff", vp, vs, th, qp, qps)
				
				fp.write(binData)
				
				count += 1
		
		fp.close()