import numpy as np
from Tool import *
from scipy.spatial import KDTree
# For the cloth type, T-shirt, it consists of 4 part, eg: front, back, right arm and left arm.
# After doing Non-rigid ICP, Map the vertices of template to the vertices of target garment.
# Then use the position of target garment to calculate the template garment vertices in 3D world.
# If the animation has f frames, need calculas f times for template vertices.


# 1. Use KD tree to find 4 closest vertices on Target garment and record its ID.
# 2. Sewing the cloth. Delete vertices and update faces.
# 3. Use the 4 closest vertices to get the 3D registration.

# Input: Registration2D, Target2D, Template3D, Target3D
# Return: Registration3D
# It is suggested that the number of vertices in target has 2 times more than template 2D/3D.
class Tshirt():
	def __init__(self):
		self.front = None
		self.back = None
		self.rightArm = None
		self.leftArm = None
		self.k = 3

	def VertexMapping(self, sourceV, targetV, sPartN, tPartN):
		# Find the K closest neighbors from targetV.
		# Return mapping(source vertex, K)
		mapping = np.zeros((1,self.k))
		for p in range(len(tPartN)-1):
			start, end = tPartN[p], tPartN[p+1]
			tree = KDTree(targetV[start:end])

			start, end = sPartN[p], sPartN[p+1]
			_, index = tree.query(sourceV[start:end], k=self.k)
			index = index.reshape(end-start, self.k)
			mapping = np.vstack([mapping, index+tPartN[p]])
		return mapping.astype(np.int32)

	def Sewing(self, templateV, mapping, rFace):
		v = templateV
		replace =  np.meshgrid(np.arange(v.shape[0]))[0] # init a array with its index  
		subtract = np.zeros(v.shape[0], dtype=np.int32)
		#deleteId = np.array([])
		mappingList = mapping.tolist()
		index = 1
		for i in v[1:-1]: # don't use last vertex because the next line 'index+1'
			same = np.where((v[index+1:] == i).all(axis=1)) # tuple(array, dtype)
			if same[0].shape[0]!=0:
				repl = same[0]
				repl = repl+index+1

				#deleteId = np.append(deleteId,repl)
				for j in repl:
					if j == replace[j]: # not yet replaced. Ex: repl=(4,58,962) are identical. next time(58,962) will wrongly delete again.
						subtract[j:] +=1
						replace[j] = index

						mappingList[index].extend(mappingList[j])
						mappingList[j] = None
			index += 1
		# Modify face
		rFace = replace[rFace]
		rFace -= subtract[rFace]
		return mappingList, rFace

	def Get3dCoordinate(self, mappingList, targetV):
		v = np.array([[0,0,0]])
		mappingList = np.array(mappingList)
		for i in mappingList:
			if i != None: # Not the deleted vertex
				newV = np.sum(targetV[i], axis=0)/len(i)
				v = np.vstack([v, newV])
		v = np.delete(v, 0, 0) # Caution: there are two abundant vertices at the first 2 vertices. 
		return v

	def checkMappingList(self, mappingList, rV, targetV):
		f = open("Check_MappingList.obj", "w")
		index = 0
		mappingList = np.array(mappingList)
		for i in mappingList:
			if index == 0 or i==None:
				index = index+1
				continue
			f.write("v %f %f %f\n" % (rV[index][0], rV[index][1], rV[index][2]) ) # From
			length = len(i)
			print(i)
			for j in range(length):
				f.write("v %f %f %f\n" % (targetV[i[j]][0], targetV[i[j]][1], targetV[i[j]][2]) ) # To
				f.write("l %d %d\n" %(index, index+j+1) )
			break
			index = index + 1
			if index >10:
				break
		f.close()

	def SaveMappingNface(self, mappingList,rFace):
		np.savez("Mapping.npz", mapping=mappingList, face=rFace, allow_pickle=True)

	def Get3DRegistration(self, template3D, registration2D, target2D, target3D):
		print('Reading obj')
		rV, rFace, rPart = ReadObj(registration2D) 
		tV, tFace, tPart = ReadObj(target2D) 
		templateV, _, _ = ReadObj(template3D)
		targetV, _, _ = ReadObj(target3D)

		print("Get 3D Registration...\n")
		mapping = self.VertexMapping(rV, tV, rPart, tPart)
		mappingList, rFace = self.Sewing(templateV, mapping, rFace)
		v3D = self.Get3dCoordinate(mappingList, targetV)
		writeObj(v3D, rFace)
		self.SaveMappingNface(mappingList,rFace)
		#self.checkMappingList(mappingList, rV, targetV)



if __name__ == '__main__':
	# folder = "Cloth/"
	# regis = ['R_Small/', 'R_Large/']
	# template3D = ['Template.obj']# know the welding part 
	# registration2D = ['LeftArm.obj',  'RightArm.obj', 'Front.obj' , 'Back.obj' ] # mapping with target2D
	# target2D =       ['LeftArmT.obj', 'RightArmT.obj','FrontT.obj', 'BackT.obj']
	# target3D = ['Small.obj'] # know the 3D coordinate
	tShirt = Tshirt()

	# Small T-Shirt
	# template3D = ['Cloth/Template.obj']# know the welding part 
	# registration2D = ['Cloth/R_Small/LeftArm.obj',  'Cloth/R_Small/RightArm.obj', 'Cloth/R_Small/Front.obj' , 'Cloth/R_Small/Back.obj' ] # mapping with target2D
	# target2D =       ['Cloth/Small/LeftArm.obj',  'Cloth/Small/RightArm.obj', 'Cloth/Small/Front.obj' , 'Cloth/Small/Back.obj']
	# target3D = ['Cloth/Small.obj'] # know the 3D coordinate
	# registration3D = tShirt.Get3DRegistration(template3D, registration2D, target2D, target3D)

	# Large T-Shirt
	# template3D = ['Cloth/Template.obj']# know the welding part 
	# registration2D = ['Cloth/R_Large/LeftArm.obj',  'Cloth/R_Large/RightArm.obj', 'Cloth/R_Large/Front.obj' , 'Cloth/R_Large/Back.obj'] # mapping with target2D
	# target2D =       ['Cloth/Large/LeftArm.obj',  'Cloth/Large/RightArm.obj', 'Cloth/Large/Front.obj' , 'Cloth/Large/Back.obj']
	# target3D = ['Cloth/Large.obj'] # know the 3D coordinate
	# registration3D = tShirt.Get3DRegistration(template3D, registration2D, target2D, target3D)

	# Medium T-Shirt
	# template3D = ['Cloth/Template.obj']# know the welding part 
	# registration2D = ['Cloth/R_Medium/LeftArm.obj',  'Cloth/R_Medium/RightArm.obj', 'Cloth/R_Medium/Front.obj' , 'Cloth/R_Medium/Back.obj'] # mapping with target2D
	# target2D =       ['Cloth/Medium/LeftArm.obj',  'Cloth/Medium/RightArm.obj', 'Cloth/Medium/Front.obj' , 'Cloth/Medium/Back.obj']
	# target3D = ['Cloth/Template.obj'] # know the 3D coordinate
	# registration3D = tShirt.Get3DRegistration(template3D, registration2D, target2D, target3D)

	# Medium T-Shirt
	template3D = ['Cloth/Template.obj']# know the welding part 
	registration2D = ['Cloth/R_Extra/LeftArm.obj',  'Cloth/R_Extra/RightArm.obj', 'Cloth/R_Extra/Front.obj' , 'Cloth/R_Extra/Back.obj'] # mapping with target2D
	target2D =       ['Cloth/Extra/LeftArm.obj',  'Cloth/Extra/RightArm.obj', 'Cloth/Extra/Front.obj' , 'Cloth/Extra/Back.obj']
	target3D = ['Cloth/Extra.obj'] # know the 3D coordinate
	registration3D = tShirt.Get3DRegistration(template3D, registration2D, target2D, target3D)



# For a unweld 3D target garment, the 2 vertices have same coordinate need to be comobined.
# Target2D is used to know the mapping ID from template to target. 
#							The welding part is one-to-one mapping.
# Target3D is used to know the 3D coordinate of template.
# The original template3D know the information of welding vertices. EX:(5,4635),(4568,7621)...
# When the welding vertices show on registration, 
#   get the middle of the 2 closest welding part on target.



