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
		
		self.hasRealIndex = self.pattern.find(PATTERN_INDEX) >= 0
		self.hasPieceIndex = self.pattern.find(PATTERN_PIECE_INDEX) >= 0
		
		self.hasReal = self.hasRealX or self.hasRealY or self.hasRealZ or self.hasRealIndex
		
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
		print "REAL INDEX DIGITS: " + str(self.realIndexDigits)
	
	def getFileName(self, indexes):
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
		
		if self.hasPieceIndex:
			index = self.calcIndexes(indexes, self.pieces)
			fileName = fileName.replace(PATTERN_PIECE_INDEX, self.padNum(index, self.pieceIndexDigits))
		
		if self.hasRealIndex:
			index = self.calcIndexes(realIndexes, self.dims)
			fileName = fileName.replace(PATTERN_INDEX, self.padNum(index, self.realIndexDigits))
		
		return fileName
	
	def calcIndexes(self, indexes, widths):
		val = 0
		prevWidth = 1
	
		for i in range(0, len(indexes)):
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