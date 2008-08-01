import struct

try:
	from meshToolsAPI import *
except:
	from meshPartitioner.meshToolsAPI import *

class MeshTools3D(MeshToolsAPI):
	
	def __init__(self, type, valsPerPoint=1):
		MeshToolsAPI.__init__(self, type, valsPerPoint)
	
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
					point = struct.unpack(self.unpackStr, binData)
					if self.valsPerPoint == 1:
						point = point[0]
					yLine.append(point)
				zLine.append(yLine)
			mesh.append(zLine)
		
		file.close()
		
		return mesh
	
	def printMesh(self, mesh, indexToPrint=None):
		"""
		Prints a string representation of the given mesh
		"""
		
		numZ = len(mesh)
		numY = len(mesh[0])
		numX = len(mesh[0][0])
		
		for y in reversed(range(0, numY)):
			for z in reversed(range(0, numZ)):
				printStr = ""
				for x in range(0, numX):
					if len(printStr) > 0:
						printStr = printStr + "\t"
					point = mesh[z][y][x]
					if indexToPrint:
						printStr = printStr + str(point[indexToPrint])
					else:
						printStr = printStr + str(point)
				print printStr
			print
	
	def writeMesh(self, mesh, fileName):
		fp = open(fileName, "wb")
		
		for yList in mesh:
			for xList in yList:
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
	
	def extractMeshPeiceFromFile(self, meshFile, dimensions, startCoords, widths):
		"""
		
		"""
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
		
		mesh = []
		
		index = 0
		
		for z in range(startZ, startZ + widthZ):
			yList = []
			for y in range(startY, startY + widthY):
				
				if debug:
					print "Y: " + str(y) + " Z: " + str(z)
				index = bytesPerZLine * z
				index += (bytesPerYLine * y) + xLineOffset
				
				if debug:
					print "index: " + str(index)
				
				file.seek(index)
				
				xList = []
				for x in range(widthX):
					binData = file.read(self.bytesPerPoint)
					point = struct.unpack(self.unpackStr, binData)
					if self.valsPerPoint == 1:
						point = point[0]
					xList.append(point)
				yList.append(xList)
			mesh.append(yList)
		
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
		
		for z in range(maxZ):
			for y in range(maxY):
				for x in range(maxX):
					if count % mod == 0:
						print str(x) + " " + str(y) + " " + str(z)
					vp = float(count)
					vs = float(x)
					th = float(y)
					qp= float(z)
					qps= float(0)
					
					binData=struct.pack("fffff", vp, vs, th, qp, qps)
					
					fp.write(binData)
					
					count += 1
					
		fp.close()

if __name__ == "__main__":
	tools = MeshTools3D(TYPE_FLOAT, 5)
	meshFile = "mesh.bin"
	dims = [4, 4, 4]
	mesh = tools.loadMesh(meshFile, dims)
	print "\nORIG\n"
	tools.printMesh(mesh)
	
	startCoords = [0, 0, 0]
	widths = [2,2,2]
	memPart = tools.extractMeshPeiceFromMemory(mesh, startCoords, widths)
	filePart = tools.extractMeshPeiceFromFile(meshFile, dims, startCoords, widths)
	
	print "\nEXTRACTED MEM\n"
	tools.printMesh(memPart)
	
	print "\nEXTRACTED FILE\n"
	tools.printMesh(filePart)
	if tools.compareMeshes(memPart, filePart):
		print "They match!"
	else:
		print "They don't match!!"