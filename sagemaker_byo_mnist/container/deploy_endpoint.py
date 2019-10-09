import boto3
import re
import os
import sys
import numpy as np
import pandas as pd
import sagemaker as sage
from sagemaker.predictor import csv_serializer
from time import gmtime, strftime

def main(image_name, s3_bucket_prefix, iam_role):

    # start the sagemaker session
    sess = sage.Session()

    # upload training data to s3
    print('uploading data to s3...')
    WORK_DIRECTORY = '../src/data/processed'
    data_location = sess.upload_data(WORK_DIRECTORY, key_prefix=s3_bucket_prefix)
    print('upload completed')

    # run the container in ecr (estimator) and train the model
    account = sess.boto_session.client('sts').get_caller_identity()['Account']
    region = sess.boto_session.region_name
    image = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(account, region, image_name)

    model = sage.estimator.Estimator(image,
                        iam_role, 1, 'ml.c4.2xlarge',
                        output_path="s3://{}/output".format(sess.default_bucket()),
                        sagemaker_session=sess)

    print('starting model training...')
    model.fit(data_location)
    print('training completed')

    # create predictor form the model (endpoint) and deploy it
    print('deploying predictor...')
    predictor = model.deploy(1, 'ml.t2.medium', serializer=csv_serializer)

    # grab some sample data
    shape = pd.read_csv("../src/data/processed/iris.csv", header=None)
    shape.drop(shape.columns[[0]],axis=1,inplace=True)
    sample = shape.sample(3)

    # make sure the predictor is working
    print('predictions:')
    print(predictor.predict(sample.values).decode('utf-8'))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])