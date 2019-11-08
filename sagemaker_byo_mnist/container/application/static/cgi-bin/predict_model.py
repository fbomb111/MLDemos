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

    print("i'm here right now")

    # temporary workaround
    tb._SYMBOLIC_SCOPE.value = True
    ###

    df = pd.read_csv(csv, header=None)
    X_test = reshapeAndNormalizeXValues(df.values)
    
    model = keras.models.load_model(os.path.join(model_path, 'model.h5'))

    y_test = model.predict(X_test)
    y_pred = np.argmax(y_test, axis=1)

    image_ids = range(1,len(X_test)+1)
    result = pd.DataFrame({'ImageId': image_ids,'Label': y_pred})
    result.to_csv(os.path.join(output_path, 'submission.csv'), index=False)
    
    return y_pred

def reshapeAndNormalizeXValues(array):
    array = array.reshape(array.shape[0], 28, 28, 1)
    array = array.astype( 'float32' )
    array = array / 255.0
    return array

if __name__ == "__main__":
    main(sys.argv[1])
