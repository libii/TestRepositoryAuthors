import os, sys, xml.dom.minidom, traceback

DEFAULT_CONF_FILE_NAME = "conf.xml"

ROOT_ELEMENT_NAME = "GridPartitionerConfiguration"

MESH_SIZE_ELEMENT_NAME = "InputMeshDimensions"
PARTITIONS_ELEMENT_NAME = "Partitions"
INPUT_MESH_ATTRIBUTE_NAME = "imputMesh"
VALS_PER_POINT_ATTRIBUTE_NAME = "valuesPerPoint"
DATA_TYPE_ATTRIBUTE_NAME = "dataType"
OUTPUT_DIR_ATTRIBUTE_NAME = "outputDir"
OUTPUT_FILE_PATTERN_ATTRIBUTE_NAME = "outputFilePattern"
INPUT_ENDIANNESS_ATT_NAME = "inputEndianness"
OUTPUT_ENDIANNESS_ATT_NAME = "outputEndianness"
VALS_TO_INCLUDE_ATT_NAME = "valuesToInclude"

class ConfLoader:
	
	def __init__(self, confFile):
		self.confFile = confFile
		self.doc = xml.dom.minidom.parse(confFile)
		self.root = self.doc.getElementsByTagName(ROOT_ELEMENT_NAME)[0]
	
	def _loadArray(self, element):
		x = int(element.getAttribute("x"))
		y = int(element.getAttribute("y"))
		try:
			z = int(element.getAttribute("z"))
			return [x, y, z]
		except:
			return [x, y]
	
	def getInputMeshDimensions(self):
		element = self.root.getElementsByTagName(MESH_SIZE_ELEMENT_NAME)[0]
		return self._loadArray(element)
	
	def getPartitions(self):
		element = self.root.getElementsByTagName(PARTITIONS_ELEMENT_NAME)[0]
		return self._loadArray(element)
	
	def getValuesPerPoint(self):
		return int(self.root.getAttribute(VALS_PER_POINT_ATTRIBUTE_NAME))
	
	def getDataType(self):
		return str(self.root.getAttribute(DATA_TYPE_ATTRIBUTE_NAME))
	
	def getInputMesh(self):
		return self.root.getAttribute(INPUT_MESH_ATTRIBUTE_NAME)
	
	def getOutputDir(self):
		return self.root.getAttribute(OUTPUT_DIR_ATTRIBUTE_NAME)
	
	def getConfFileName(self):
		return os.path.abspath(self.confFile)
	
	def getFileNamePattern(self):
		return self.root.getAttribute(OUTPUT_FILE_PATTERN_ATTRIBUTE_NAME)
	
	def getInputEndianness(self):
		try:
			return self.evalEndianness(self.root.getAttribute(INPUT_ENDIANNESS_ATT_NAME))
		except:
			sys.stderr.write("WARNING: Input Endianness not specified, using native\n")
			return "="
	
	def getOutputEndianness(self):
		try:
			return self.evalEndianness(self.root.getAttribute(OUTPUT_ENDIANNESS_ATT_NAME))
		except:
			sys.stderr.write("WARNING: Output Endianness not specified, using native\n")
			return "="
	
	def evalEndianness(self, end):
		end = str(end)
		end = end.lower()
		end = end.strip()
		if end.startswith("l"):
			return "<"
		if end.startswith("b"):
			return ">"
		return "="
	
	def getValuesToInclude(self, valsStr=None):
		if valsStr == None:
			valsStr = str(self.root.getAttribute(VALS_TO_INCLUDE_ATT_NAME))
		try:
			valsStr = valsStr.strip()
			vals = valsStr.split(',')
			valInts = []
			for val in vals:
				valInts.append(int(val))
			return valInts
		except:
			#traceback.print_exception(*sys.exc_info())
			return None
	
	def printConfiguration(self):
		print "Mesh Partitioner Configuration"
		print "(loaded from " + self.confFile + ")"
		print
		print "Input Mesh: " + self.getInputMesh()
		print "Input Mesh Dimensions: " + str(self.getInputMeshDimensions())
		print "Partitions: " + str(self.getPartitions())
		print
		print "Values Per Point: " + str(self.getValuesPerPoint())
		print "Data Type: " + self.getDataType()

if __name__ == "__main__":
	conf = ConfLoader("../../" + DEFAULT_CONF_FILE_NAME)
	conf.printConfiguration()