import codecs
import sys
import numpy as np
lib=__import__("lib1772576")


def run(array):
    num_cluster=int(array[len(array)-1])
    string=str(array[len(array)-2])
    files=[]
    for i in range(len(array)-2):
        files.append(array[i])
    points=[lib.char_freq(f,string) for f in files]
    clusters=lib.single(points,num_cluster)
    print (clusters)

arguments=sys.argv[1:]
run(arguments)
