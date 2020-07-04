import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
#tf.executing_eagerly()
import pickle
import sys
import time
import datetime
import numpy as np

def Allign(data):
	n = data.shape[0]
	data = data.reshape(n,-1,3)
	for i in range(n):
		cloth = data[i]
		mean = cloth.mean(axis=0)
		cloth = cloth-mean
		data[i] = cloth
		#print(data[i],mean)
	return data.reshape(n,-1)

data = np.load("Cloth+.npy")
data = Allign(data)
mean = data.mean(axis=0)
std  = data.std(axis=0)
data = (data-mean)/std

model = tf.keras.models.load_model('Encoder+')
model.evaluate(data,data)

one = model.get_layer(name='Input')(data)
latentCode = model.get_layer(name='Latent')(one)
np.save("Data/ClothLatentCode+.npy", latentCode.numpy())

# print(data)
# result = model.predict(data)
# print(result)