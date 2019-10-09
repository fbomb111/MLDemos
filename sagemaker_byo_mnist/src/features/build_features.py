import pandas as pd
import numpy as np
import keras

def main():
    train = pd.read_csv('src/data/external/train.csv')
    test = pd.read_csv('src/data/external/test.csv')

    # Convert df to values
    train_values = train.values[:, 1:]
    test_values = test.values

    # Reshape and normalize training data
    X_train = reshapeAndNormalizeXValues(train_values)
    X_test = reshapeAndNormalizeXValues(test_values)

    # one hot encoding
    number_of_classes = 10
    y_train = train.values[:,0]
    y_train = keras.utils.to_categorical(y_train, number_of_classes)

    path = 'src/data/processed/'
    np.save(path + 'X_train.npy', X_train)
    np.save(path + 'X_test.npy', X_test)
    np.save(path + 'y_train.npy', y_train)

def reshapeAndNormalizeXValues(array):
    array = array.reshape(array.shape[0], 28, 28, 1)
    array = array.astype( 'float32' )
    array = array / 255.0
    return array

if __name__ == "__main__":
    main()