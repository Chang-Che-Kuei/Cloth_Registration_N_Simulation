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
	#tf.print(y_pred[0,0,10:15], y_true[0,0,10:15])
	error = tf.math.reduce_mean(tf.math.square(y_true-y_pred))
	return error


data = np.load("Data/Data0621_Pose.npz",allow_pickle=True)
from sklearn.utils import shuffle
x = data['x']
y = data['y']
x, y = shuffle(x, y, random_state=0)

batchSize = 128
InSize = x.shape[1] # 82
OutSize = y.shape[1] # template vertices*3
print(x.shape, y.shape)
trainX, trainY = x[:-32], y[:-32]
evaX, evaY = x[-32:], y[-32:]

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(256, input_shape=(InSize,), activation='relu' ) )
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(1024, activation='relu') )
model.add(tf.keras.layers.Dense(OutSize))

RMSprop = tf.keras.optimizers.RMSprop(learning_rate=0.001)
Adam    = tf.keras.optimizers.Adam(learning_rate=0.0003)
SGD = tf.keras.optimizers.SGD(learning_rate=1)
model.compile(optimizer=Adam,
              loss=MSE)#'mean_squared_error')

log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
model.fit(trainX, trainY, batch_size=batchSize, epochs=350, validation_data=(evaX, evaY)) #callbacks=[tensorboard_callback] )

model.summary()
model.save('ClothPoseNet')
# start = time.perf_counter()
# result = model.predict(x)
# elapsed = time.perf_counter() - start
# print('Model %.3f seconds.' % elapsed)
#print(result.shape)
#print(result[0,0,:10],'\n', x[0,0,:10],'\n', result[-1,0,:10],'\n', x[0,0,:10])

# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=5)

'''
inputs = tf.random.normal([32, 10, 8])
gru = tf.keras.layers.GRU(5, return_sequences=True)
output = gru(inputs)
print(output)
'''

'''
class ClothNet(tf.keras.Model):
	def __init__(self):
		super(ClothNet, self).__init__()
		self.lay0 = 
'''