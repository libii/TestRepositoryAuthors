# INTEGERS
TYPE_UNSIGNED_SHORT	 	= "H"	# 2 bytes
TYPE_SHORT 				= "h"	# 2 bytes
TYPE_UNSIGNED_INT	 	= "I"	# 4 bytes
TYPE_INT 				= "i"	# 4 bytes
TYPE_UNSIGNED_LONG	 	= "L"	# 8 bytes
TYPE_LONG 				= "l"	# 8 bytes

# FLOATING
TYPE_FLOAT 				= "f"	# 4 bytes
TYPE_DOUBLE 			= "d"	# 8 bytes

class MeshToolsAPI:
	
	def __init__(self, type, valsPerPoint=1):
		
		self.type = type
		self.valsPerPoint = valsPerPoint
		
		# detect the type
		if type in (TYPE_UNSIGNED_SHORT, TYPE_SHORT):
			self.bytesPerNum = 2
		elif type in (TYPE_UNSIGNED_INT, TYPE_INT, TYPE_FLOAT):
			self.bytesPerNum = 4
		elif type in (TYPE_UNSIGNED_LONG, TYPE_LONG, TYPE_DOUBLE):
			self.bytesPerNum = 8
		else:
			raise CustomException("Binary number type '" + type + "' is unknown or unsupported!")
		
		self.bytesPerPoint = self.bytesPerNum * self.valsPerPoint
		self.unpackStr = ""
		for i in range(0, self.valsPerPoint):
			self.unpackStr = self.unpackStr + self.type
	
	def loadMesh(self, meshFile, dimensions):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def printMesh(self, mesh, indexToPrint=None, warn=True):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def writeMesh(self, mesh, fileName):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def extractMeshPeiceFromMemory(self, origMesh, startCoords, widths):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def extractMeshPeiceFromFile(self, meshFile, dimensions, startCoords, widths, outFile=None):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def compareMeshes(self, mesh1, mesh2):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def writeTestMesh(self, fileName, widths):
		raise MeshException("ERROR: Mesh function not implemented!")
	
	def isAnyDimLengthGreaterThan(self, dims, val):
		for dim in dims:
			if dim > val:
				return True
		return False
	
	def checkPrintWarn(self, dims):
		val = 10
		if self.isAnyDimLengthGreaterThan(dims, val):
			response = ""
			while not (response.startswith("y") or response.startswith("n")):
				print "WARNING: You are trying to print a very large mesh: " + str(dims)
				response = raw_input("Print anyways? (y/n) ").lower()
			if response.startswith("n"):
				return False
		return True
			
		

class MeshException(Exception):
	def __init__(self, value):
		self.parameter = value
	
	def __str__(self):
		return repr(self.parameter)