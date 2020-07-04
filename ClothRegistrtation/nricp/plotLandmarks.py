import numpy as np

def LoadObj(filename):
	# Load Obj
	f = open(filename, "r")

	v = np.array([[0,0,0]])
	line = f.readline()
	while line:
		if line[0:2] == "v ":
			vertex = [float(i) for i in line[2:].split()]
			v = np.vstack([v, vertex])
		line = f.readline()
	f.close()
	return v

vS = LoadObj("NewTemplate.obj")
vT = LoadObj("NewTarget.obj")

f = open("Landmarks.obj","w")
landS = [3873,4169,1956,375,1848,56,2058,9,3419,3984]
landT = [4900,5182,2635,455,2378,175,2238,3,4414,5123]
for i in landS:
	f.write("v %f %f %f\n" % (vS[i][0], vS[i][1], vS[i][2]) )
f.write("l %d %d %d %d %d %d %d %d %d %d\n" % (1,2,3,4,5,6,7,8,9,10) )
for i in landT:
	f.write("v %f %f %f\n" % (vT[i][0]+2, vT[i][1], vT[i][2]) )
f.write("l %d %d %d %d %d %d %d %d %d %d\n" % (11,12,13,14,15,16,17,18,19,20) )
f.close()