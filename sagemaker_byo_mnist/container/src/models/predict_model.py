import pandas as pd
import numpy as np
import keras
import sys 
import pickle
import os

# temporary workaround
import keras.backend.tensorflow_backend as tb
###

output_path = 'output'
model_path = os.path.join(output_path, 'models')

def main(csv):

    # temporary workaround
    tb._SYMBOLIC_SCOPE.value = True
    ###

    if os.path.basename(os.path.normpath(os.getcwd())) != 'container':
        os.chdir('container')

    X_test = reshapeAndNormalizeXValues(csv)
    model = keras.models.load_model(os.path.join(model_path, 'model.h5'))
    y_test = model.predict(X_test)
    return y_test

def outputCSVPredictionsToKaggle(csv):
    y_test = main(csv)
    y_pred = np.argmax(y_test, axis=1)
    length = len(reshapeAndNormalizeXValues(csv))
    image_ids = range(1,length+1)
    result = pd.DataFrame({'ImageId': image_ids,'Label': y_pred})
    result.to_csv(os.path.join(output_path, 'submission.csv'), index=False)

def reshapeAndNormalizeXValues(array):
    # channels first or last?
    array = array.reshape(array.shape[2], 28, 28, 1)
    array = array.astype( 'float32' )
    array = array / 255.0
    return array

if __name__ == "__main__":
    main(sys.argv[1])
