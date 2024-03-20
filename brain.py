from keras.layers import Dense
from keras import Sequential, models
import numpy as np
import random

WIN_HEIGHT = 480
WIN_WIDTH = 640
MAX_TOT_WIDTH = 25 * 3
RATE = 0.2


class Brain:
    def __init__(self, model):
        if model:
            self.model = model.copy()
        else:
            self.model = Sequential()
            self._model_init()

    def _model_init(self):
        self.model.add(Dense(2, input_shape=(1,)))
        self.model.add(Dense(8))
        self.model.add(Dense(1))
        self.model.compile(optimizer="adam", loss="mse")

    def think(self, distance, width):
        return self.model(np.array([distance, width]), training=False)

    def copy(self):
        new_model = models.clone_model(self.model)
        new_model.compile(optimizer="adam", loss="mse")
        new_model.set_weights(self.model.get_weights())
        return new_model

    def mutate(self):
        weights = self.model.get_weights()
        for values in weights:
            for value in values:
                if random.random() < RATE:
                    value += np.random.normal()

        self.model.set_weights(weights)
