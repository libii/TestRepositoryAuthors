from meshPartitioner.mesh2D.meshTools2D import MeshTools2D
from meshPartitioner.mesh2D.meshTools2D import TYPE_FLOAT

meshTools = MeshTools2D(TYPE_FLOAT, 5)
tests = []

import test_01_copy
tests.append(test_01_copy.Test(meshTools))


numFails = 0
numTests = 0

for test in tests:
	result = test.test_catch()
	
	if result:
		print "SUCCESS: " + test.getName()
	else:
		numFails += 1
		print "FAILURE: " + test.getName()
	numTests += 1

if numFails == 0:
	print "All " + str(numTests) + " tests completed successfully!"
else:
	print str(numTests - numFails) + " of " + str(numTests) + " completed successfully."