
import os

def rmdir(dir, verbose=False):
    items = os.listdir(dir)
    for item in items:
        if item == '.' or item == '..': continue
        file = dir + os.sep + item
        if os.path.isdir(file):
            # if this file is actually a dir, delete the dir
            rmdir(file, verbose)
        else: # it's just a file
            if verbose:
                print "Deleting " + file 
            os.remove(file)
    os.rmdir(dir)