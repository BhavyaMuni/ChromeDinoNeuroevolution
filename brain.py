import tensorflow as tf
from keras.layers import Dense
from keras import Sequential
import math
import numpy as np
import random
from copy import copy
WIN_HEIGHT = 480
WIN_WIDTH = 640
MAX_TOT_WIDTH = 25*3
RATE = 0.2

# tf.config.run_functions_eagerly(False)
tf.compat.v1.disable_eager_execution()


class Brain:
    def __init__(self, model):
        if model != None:
            self.model = model.copy()
        else:
            self.model = Sequential()
            self._model_init()

    def _model_init(self):
        self.model.add(Dense(2, input_shape=(1,)))
        self.model.add(Dense(8, activation='sigmoid'))
        self.model.add(Dense(1, activation='tanh'))
        self.model.compile(optimizer='adam', loss='mse')

    def think(self, closest):
        cactus_x = closest.x/WIN_WIDTH
        cactus_width = closest.total_width/MAX_TOT_WIDTH
        return self.model.predict([cactus_x, cactus_width])

    def copy(self):
        return copy(self.model)

    def mutate(self):
        weights = self.model.get_weights()
        for values in weights:
            for value in values:
                if random.random() < RATE:
                    value += np.random.normal()

        self.model.set_weights(weights)
