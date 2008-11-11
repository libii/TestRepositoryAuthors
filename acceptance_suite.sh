#! /bin/bash
# This script creates a mesh, partitions the mesh
#and compares the eight partitions created with 8 reference_values.
/bin/cp conf.xml conf.xml.save
/bin/cp conf.xml.master conf.xml
/bin/rm -rf mesh_10_10_10.bin_2_2_2
/bin/rm mesh_10_10_10.bin
/bin/rm tests/*
echo  ""
./makeTestMesh.py  -a 10 10 10 
echo  ""
./partition.py
echo  ""
/bin/cp conf.xml.save conf.xml
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_0_0_0.bin  tests/mesh_0_0_0.bin  
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_0_0_1.bin  tests/mesh_0_0_1.bin 
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_0_1_0.bin  tests/mesh_0_1_0.bin  
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_0_1_1.bin  tests/mesh_0_1_1.bin
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_1_0_0.bin  tests/mesh_1_0_0.bin 
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_1_0_1.bin  tests/mesh_1_0_1.bin  
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_1_1_0.bin  tests/mesh_1_1_0.bin  
/bin/cp mesh_10_10_10.bin_2_2_2/mesh_1_1_1.bin  tests/mesh_1_1_1.bin
echo  ""
./acceptance.py
