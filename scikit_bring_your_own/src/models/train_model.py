import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
import numpy as np
import pandas as pd
import os
from sklearn import tree
import sys

def main(input_files, params):

    raw_data = [ pd.read_csv(file, header=None) for file in input_files ]
    train_data = pd.concat(raw_data)

    # labels are in the first column
    train_y = train_data.ix[:,0]
    train_X = train_data.ix[:,1:]

    # Here we only support a single hyperparameter. Note that hyperparameters are always passed in as
    # strings, so we need to do any necessary conversions.
    max_leaf_nodes = params.get('max_leaf_nodes', None)
    if max_leaf_nodes is not None:
        max_leaf_nodes = int(max_leaf_nodes)

    # Now use scikit-learn's decision tree classifier to train the model.
    model = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)
    model = model.fit(train_X, train_y)

    return model 

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])