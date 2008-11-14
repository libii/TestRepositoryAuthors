#! /bin/bash
# This script creates a mesh, partitions the mesh
#and compares the eight partitions created with 8 reference_values.
/bin/rm tests/*
echo  ""
./makeTestMesh.py -c conf.xml.master -a 10 10 10 
echo  ""
./partition.py -c conf.xml.master
echo  ""
./acceptance.py
