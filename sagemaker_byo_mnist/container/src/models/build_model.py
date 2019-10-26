import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
import numpy as np
import os

data_path = 'data/processed'

def main():
    model=Sequential()

    model.add(Conv2D(32,3, activation='relu'))
    model.add(Conv2D(32,3, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))

    model.add(Conv2D(64,3, activation='relu'))
    model.add(Conv2D(64,3, activation='relu'))
    model.add(MaxPooling2D(pool_size=2))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

    X_train = np.load(os.path.join(data_path, 'X_train.npy'))
    y_train = np.load(os.path.join(data_path, 'y_train.npy'))

    model.fit(X_train, y_train,
            epochs=2,
            batch_size=128,
            verbose=True)

    return model 

if __name__ == "__main__":
    main()