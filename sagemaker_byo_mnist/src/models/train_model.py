import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
import numpy as np
import pandas as pd
import sys

def main(input_files, params):

    # raw_data = [ pd.read_csv(file, header=None) for file in input_files ]
    # train_data = pd.concat(raw_data)

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

    path = 'src/data/processed/'
    X_train = np.load(path + 'X_train.npy')
    y_train = np.load(path + 'y_train.npy')

    model.fit(X_train, y_train,
            epochs=20,
            batch_size=128,
            verbose=True)

    return model

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])