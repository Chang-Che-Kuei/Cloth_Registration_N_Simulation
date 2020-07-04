import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
#tf.executing_eagerly()
import pickle
import sys
import time
import datetime
import numpy as np
import os

data = np.load("Data/Data0619--O.npz",allow_pickle=True)
x = data['x']
y = data['y']
evaX = np.expand_dims(np.array(x[1][:,-85:-3]), axis=0) # Female_Short_Run_Medium_R
evaY = np.expand_dims(np.array(y[1]), axis=0)

model = tf.keras.models.load_model('ClothNet+')
model.evaluate(evaX, evaY)


result = model(evaX)

savePath = 'Result/0621_2/'
os.mkdir(savePath)
print(result.shape)
cloth = result.numpy().reshape( result.shape[1], -1,3)
face = np.load("face.npy")
for i in range(cloth.shape[0]):
	now = cloth[i]
	print(now.shape)
	f = open(savePath + str(i).zfill(4) + '.obj' , "w")
	for v in now:
		f.write('v %f %f %f\n' % (v[0], v[1], v[2]+i*0.4))
	for fa in face:
		f.write('f %d %d %d\n' % (fa[0], fa[1], fa[2]))
	f.close()
