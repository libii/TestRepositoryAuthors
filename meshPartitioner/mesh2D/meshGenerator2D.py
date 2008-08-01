import os, struct

fileName = "mesh.bin"

fp = open(fileName, "wb")

count = 0

maxX = 4
maxY = 4

for y in range(maxY):
	for x in range(maxX):
		print str(x) + " " + str(y)
		vp = float(count)
		vs = float(x)
		th = float(y)
		qp= float(0)
		qps= float(0)
		
		binData=struct.pack("fffff", vp, vs, th, qp, qps)
		
		fp.write(binData)
		
		count += 1

fp.close()