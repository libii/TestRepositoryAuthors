#!/usr/bin/env python

import xml.dom.minidom

import os

import meshPartitioner.conf.confLoader as confLoader

# ============ DEFAULTS ============

confFileName = confLoader.DEFAULT_CONF_FILE_NAME

# the input mesh
#inputMesh = "/scratch/00392/yfcui/Shakeout/so2.1-ds-6k/mesh100m.out.bigend.q50"
inputMesh = "/gpfs-wan/projects/SCEC/cvm/mesh100m.out.bigend.q50"
#inputMesh = "mesh_16_16_16.bin"

# output dir. if blank, the directory name will be: meshName_xPieces_yPieces_zPieces (in the current directory)
outputDir = ""

# the number of values per data point
valuesPerPoint = 5

fileNamePattern = "media%I.bin"
#fileNamePattern = "mesh_%X_%Y_%Z.bin"

# type of numbers for each value:
# f = float
# d = double
# h = short
# H = unsigned short
# i = int
# I = unsinged in
# l = long
# L = unsigned long
dataType = "f"

# the size of the input mesh
meshSizeX = 6000
meshSizeY = 3000
meshSizeZ = 800
#meshSizeX = 4
#meshSizeY = 4
#meshSizeZ = 4

# number of partitions in each dimension. this must be evenly divisible by the
# size of that dimension
partitionsX = 40
partitionsY = 40
partitionsZ = 10
#partitionsX = 2
#partitionsY = 2
#partitionsZ = 2

# ============ Write to File ============

# create xml doc
xml_doc = xml.dom.minidom.Document()

# create a root
root = xml_doc.createElement(confLoader.ROOT_ELEMENT_NAME)

# add the root to the doc
xml_doc.appendChild(root)

# Input Mesh Size
inputMeshSize = xml_doc.createElement(confLoader.MESH_SIZE_ELEMENT_NAME)
inputMeshSize.setAttribute("x", str(meshSizeX))
inputMeshSize.setAttribute("y", str(meshSizeY))
inputMeshSize.setAttribute("z", str(meshSizeZ))
root.appendChild(inputMeshSize)

# Partitions
partitions = xml_doc.createElement(confLoader.PARTITIONS_ELEMENT_NAME)
partitions.setAttribute("x", str(partitionsX))
partitions.setAttribute("y", str(partitionsY))
partitions.setAttribute("z", str(partitionsZ))
root.appendChild(partitions)

root.setAttribute(confLoader.INPUT_MESH_ATTRIBUTE_NAME, inputMesh)
root.setAttribute(confLoader.VALS_PER_POINT_ATTRIBUTE_NAME, str(valuesPerPoint))
root.setAttribute(confLoader.DATA_TYPE_ATTRIBUTE_NAME, dataType)
root.setAttribute(confLoader.OUTPUT_DIR_ATTRIBUTE_NAME, outputDir)
root.setAttribute(confLoader.OUTPUT_FILE_PATTERN_ATTRIBUTE_NAME, fileNamePattern)


file_object = open(confFileName, "w")
xml_doc.writexml(file_object , "    ", " ", "\n", "UTF-8")
file_object.close()

os.system("cat " + confFileName)