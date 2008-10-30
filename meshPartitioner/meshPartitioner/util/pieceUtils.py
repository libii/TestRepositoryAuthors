import meshPartitioner.meshToolsAPI as meshTools

def loadPieceWidths(dimensions, pieces):
	if len(pieces) != len(dimensions):
		raise meshTools2D.MeshException("You must specify the number of pieces for each dimension!")
	
	pieceWidths = []
	for i in range(0, len(pieces)):
		width = dimensions[i]
		numPieces = pieces[i]
		
		if width % numPieces != 0 or numPieces > width:
			raise meshTools.MeshException("Width of dimension " + str(i+1) + ": " + str(width)\
										+ " cannot be evenly divided into " + str(numPieces) + ".")
		
		pieceWidths.append(width / numPieces)
	
	return pieceWidths

PATTERN_X_INDEX = "%x"
PATTERN_Y_INDEX = "%y"
PATTERN_Z_INDEX = "%z"
PATTERN_X_PIECE_INDEX = "%X"
PATTERN_Y_PIECE_INDEX = "%Y"
PATTERN_Z_PIECE_INDEX = "%Z"
PATTERN_INDEX = "%i"
PATTERN_PIECE_INDEX = "%I"
PATTERN_MPI_RANK_INDEX = "%R"
PATTERN_ORIGINAL_NAME = "%n"

class PieceNameGenerator:
	
	def __init__(self, originalBaseName, pattern, dimensions, pieces, pieceWidths):
		self.originalBaseName = originalBaseName
		self.pattern = pattern
		self.dims = dimensions
		self.pieces = pieces
		self.pieceWidths = pieceWidths
		
		# because the original base name never changes, we can do that replacement now
		self.pattern = self.pattern.replace(PATTERN_ORIGINAL_NAME, self.originalBaseName)
		
		self.hasRealX = self.pattern.find(PATTERN_X_INDEX) >= 0
		self.hasRealY = self.pattern.find(PATTERN_Y_INDEX) >= 0
		self.hasRealZ = self.pattern.find(PATTERN_Z_INDEX) >= 0
		
		self.realNum, self.realNumStr = self.getNumFlag(PATTERN_INDEX, self.pattern)
		self.pieceNum, self.pieceNumStr = self.getNumFlag(PATTERN_PIECE_INDEX, self.pattern)
		self.mpiNum, self.mpiNumStr = self.getNumFlag(PATTERN_MPI_RANK_INDEX, self.pattern)
		
		self.hasReal = self.hasRealX or self.hasRealY or self.hasRealZ or (self.realNum >= 0)
		
		self.indIndexDigits = 0
		for i in range(len(pieces)):
			piece = pieces[i] - 1
			if piece > self.indIndexDigits:
				self.indIndexDigits = piece
		self.indIndexDigits = len(str(self.indIndexDigits))
		
		maxIndex = []
		for index in pieces:
			maxIndex.append(index - 1)
		self.pieceIndexDigits = len(str(self.calcIndexes(maxIndex, pieces)))
		
		self.realIndIndexDigits = 0
		for i in range(len(dimensions)):
			piece = dimensions[i] - 1
			if piece > self.realIndIndexDigits:
				self.realIndIndexDigits = piece
		self.realIndIndexDigits = len(str(self.realIndIndexDigits))
		
		maxIndex = []
		for index in dimensions:
			maxIndex.append(index - 1)
		self.realIndexDigits = len(str(self.calcIndexes(maxIndex, dimensions)))
	
	def getFileName(self, indexes, zyx=False):
		fileName = self.pattern
		
		fileName = fileName.replace(PATTERN_X_PIECE_INDEX, self.padNum(indexes[0], self.indIndexDigits))
		fileName = fileName.replace(PATTERN_Y_PIECE_INDEX, self.padNum(indexes[1], self.indIndexDigits))
		fileName = fileName.replace(PATTERN_Z_PIECE_INDEX, self.padNum(indexes[2], self.indIndexDigits))
		
		if self.hasReal:
			realIndexes = []
			realX = indexes[0] * self.pieceWidths[0]
			realIndexes.append(realX)
			realY = indexes[1] * self.pieceWidths[1]
			realIndexes.append(realY)
			if len(indexes) == 3:
				realZ = indexes[2] * self.pieceWidths[2]
				realIndexes.append(realZ)
		
		if self.hasRealX:
			fileName = fileName.replace(PATTERN_X_INDEX, self.padNum(realX, self.realIndIndexDigits))
		if self.hasRealY:
			fileName = fileName.replace(PATTERN_Y_INDEX, self.padNum(realY, self.realIndIndexDigits))
		if self.hasRealX:
			fileName = fileName.replace(PATTERN_Z_INDEX, self.padNum(realZ, self.realIndIndexDigits))
		
		if self.pieceNum >= 0:
			index = self.calcIndexes(indexes, self.pieces, zyx=zyx)
			if self.pieceNum == 0:
				num = self.pieceIndexDigits
			else:
				num = self.pieceNum
			fileName = fileName.replace(self.pieceNumStr, self.padNum(index, num))
		
		if self.mpiNum >= 0:
			index = self.calcIndexes(indexes, self.pieces, zyx=True)
			if self.mpiNum == 0:
				num = self.pieceIndexDigits
			else:
				num = self.mpiNum
			fileName = fileName.replace(self.mpiNumStr, self.padNum(index, num))
		
		if self.realNum >= 0:
			index = self.calcIndexes(realIndexes, self.dims, zyx=zyx)
			if self.realNum == 0:
				num = self.realIndexDigits
			else:
				num = self.realNum
			fileName = fileName.replace(self.realNumStr, self.padNum(index, num))
		
		return fileName
	
	def getNumFlag(self, flag, name):
		flagChar = flag[len(flag)-1]
		#print "FLAG CHAR: " + flagChar
		
		numStr = "0"
		
		i = name.find("%")
		while i >= 0:
			name = name[i:]
			
			if name[1] == flagChar:
				#print "returning: 0 " + name[0:1]
				return 0, name[0:2]
			
			if name[2] == flagChar:
				try:
					num = int(name[1])
					#print "returning: " + str(num) + " " + name[0:2]
					return num, name[0:3]
				except:
					name = name[2:]
					i = name.find("%")
					continue
			name = name[2:]
			i = name.find("%")
		
		return -1, flag
	
	def calcIndexes(self, indexes, widths, zyx=False):
		"""
		1*X + xWidth * Y + (xWidth * yWidth) * Z
		"""
		
		indexList = range(0, len(indexes))
		if zyx:
			indexList.reverse()
		
		val = 0
		prevWidth = 1
	
		for i in indexList:
			index = indexes[i]
			valToAdd = prevWidth * index
			val += valToAdd
			prevWidth = widths[i] * prevWidth
		
		return val
	
	def padNum(self, num, digits):
		numStr = str(num)
		
		while len(numStr) < digits:
			numStr = "0" + numStr
		
		return numStr

if __name__ == "__main__":
	dimensions = (4, 4, 4)
	pieces = (2, 2, 2)
	pieceWidths = (2, 2, 2)
	
	pattern = "media%I.bin"
	#pattern = "media%X_%Y_%Z.bin"
	gen = PieceNameGenerator("", pattern, dimensions, pieces, pieceWidths)
	print gen.getFileName((2, 1, 0))