import tensorflow as tf
from tensorflow.keras.layers import Dense
import math
import numpy as np
import random

WIN_HEIGHT = 480
WIN_WIDTH = 640
MAX_TOT_WIDTH = 25*3


class Brain:
    def __init__(self, model):
        if model != None:
            self.model = model.copy()
        else:
            self.model = tf.keras.Sequential()
            self._model_init()

    def _model_init(self):
        self.model.add(Dense(8, input_shape=(1,)))
        self.model.add(Dense(1, activation='tanh'))

    def think(self, closest):
        cactus_x = closest.x/WIN_WIDTH
        cactus_width = closest.total_width/MAX_TOT_WIDTH
        return self.model.predict([cactus_x, cactus_width])

    def copy(self):
        weights = self.model.get_weights()
        new_model = tf.keras.Sequential()
        new_model.add(Dense(8, input_shape=(1,)))
        new_model.add(Dense(1, activation='tanh'))
        new_model.set_weights(weights)
        return new_model

    def mutate(self, rate):
        weights = self.model.get_weights()
        for values in weights:
            for value in values:
                if random.random() < rate:
                    value += np.random.normal()

        self.model.set_weights(weights)
