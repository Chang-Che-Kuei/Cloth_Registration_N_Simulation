import numpy as np


def ReadObj(fileList):
	v = np.array([[0,0,0]])
	face = np.array([[0,0,0]])
	Accumulate = 0 # combine all the vertices and make indices right
	partRegion = [1]
	for file in fileList:
		with open(file, 'r') as f:
			line = f.readline()
			while line:
				if line[0:2] == "v ":
					vertex = [float(i) for i in line[2:].split()]
					v = np.vstack([v, vertex])

				elif line[0:2] == "f ":
					line = line[1:].split() # eg: ['187/187/187', '13/13/13', '12/12/12']
					newface = [ int(i.split('/')[0])+Accumulate for i in line ]
					face = np.vstack([face, newface])
				line = f.readline()
			Accumulate = v.shape[0]-1
			partRegion.append(Accumulate+1)
	return v, face, partRegion

def writeObj(v3D, rFace):
	f = open("3D_Registration_SewAndMap.obj", "w")
	for i in range(1,v3D.shape[0]):
		f.write("v %f %f %f\n" % (v3D[i][0], v3D[i][1], v3D[i][2]) )
	for i in range(1,rFace.shape[0]):
		f.write("f %d %d %d\n" % (rFace[i][0], rFace[i][1], rFace[i][2]) )
	f.close()

