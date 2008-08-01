import os, sys, traceback

class Test:
	
	mesh_list = []
	
	def __init__(self, meshTools, name, verbose=False):
		self.meshTools = meshTools
		self.name = name
		self.verbose = verbose
		
		meshList = os.listdir(".")
		
		for file in meshList:
			if not os.path.isfile(file):
				continue
			if not file.endswith(".bin"):
				continue
			if file.count("_") < 1:
				continue
			self.mesh_list.append(file)
	
	def test(self):
		print "ERROR: No test implemented!"
		return False
	
	def test_catch(self):
		try:
			return self.test()
		except:
			traceback.print_exception(*sys.exc_info())
			return False
	
	def getName(self):
		return self.name
	
	def extractSizeFromMeshName(self, meshFile):
		meshFile = meshFile.replace(".bin", "")
		fileSplit = meshFile.split("_")
		yIndex = int(fileSplit[len(fileSplit) - 1])
		xIndex = int(fileSplit[len(fileSplit) - 2])
		
		return (xIndex, yIndex)