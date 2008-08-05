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