import pandas as pd
import numpy as np
import keras

def main():
    model = keras.models.load_model('models/model.h5')

    path = 'src/data/processed/'
    X_test = np.load(path + 'X_test.npy')

    y_test = model.predict(X_test)
    y_pred = np.argmax(y_test, axis=1)

    image_ids = range(1,len(X_test)+1)
    result = pd.DataFrame({'ImageId': image_ids,'Label': y_pred})
    result.to_csv('src/data/processed/submission.csv', index=False)

if __name__ == "__main__":
    main()
