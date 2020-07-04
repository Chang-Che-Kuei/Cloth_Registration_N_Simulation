import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
#tf.executing_eagerly()
import pickle
import sys
import time
import datetime
import numpy as np

def MSE( y_true, y_pred):
	#tf.print(y_pred[0,0,:5])
	error = tf.math.reduce_mean(tf.math.square(y_true-y_pred))
	return error

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

data = np.load("Cloth+.npy")# Large Medium Small (3, 41271)
print(data.shape)
data = Allign(data)
mean = data.mean(axis=0)
std  = data.std(axis=0)
data = (data-mean)/std # standardization
batch = data.shape[0]
Dim = data.shape[1]

#data = data[0:1]
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(256, input_shape=(Dim,), name='Input' ))
#model.add(tf.keras.layers.Dense(256 , name='Layer1'))
model.add(tf.keras.layers.Dense(20 ,name='Latent'  ))
#model.add(tf.keras.layers.Dense(256 ))
model.add(tf.keras.layers.Dense(256 ))
model.add(tf.keras.layers.Dense(Dim ))

RMSprop = tf.keras.optimizers.RMSprop(learning_rate=0.001)
adam = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer='sgd',
              loss='mean_squared_error')#'mean_squared_error')
model.fit(data, data, epochs=5020, batch_size=1)
model.summary()
model.save('Encoder+')


# one = model.get_layer(name='Input')(data)
# two = model.get_layer(name='Layer1')(one)
# latentCode = model.get_layer(name='Latent')(two)
# print(latentCode.numpy())
# tf.print(model.layers[0].output)