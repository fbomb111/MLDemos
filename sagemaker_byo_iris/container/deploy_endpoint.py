# S3 bucket prefix
prefix = 'arn:aws:s3:::sagemaker-us-east-2-117588387775'

# IAM Role with sagemaker permissions
role = 'arn:aws:iam::117588387775:role/service-role/AmazonSageMaker-ExecutionRole-20190513T204887'

import boto3
import re
import os
import numpy as np
import pandas as pd
import sagemaker as sage
from sagemaker.predictor import csv_serializer
from time import gmtime, strftime

# start the sagemaker session
sess = sage.Session()

# upload training data to s3
WORK_DIRECTORY = '../src/data/processed'
data_location = sess.upload_data(WORK_DIRECTORY, key_prefix=prefix)

# run the container in ecr (estimator) and train the model
account = sess.boto_session.client('sts').get_caller_identity()['Account']
region = sess.boto_session.region_name
image = '{}.dkr.ecr.{}.amazonaws.com/application-sample:latest'.format(account, region)

tree = sage.estimator.Estimator(image,
                       role, 1, 'ml.c4.2xlarge',
                       output_path="s3://{}/output".format(sess.default_bucket()),
                       sagemaker_session=sess)

tree.fit(data_location)

# create predictor form the model (endpoint) and deploy it
predictor = tree.deploy(1, 'ml.t2.medium', serializer=csv_serializer)

# grab some sample data
shape = pd.read_csv("../src/data/processed/iris.csv", header=None)
shape.drop(shape.columns[[0]],axis=1,inplace=True)
sample = shape.sample(3)

# make sure the predictor is working
print(predictor.predict(sample.values).decode('utf-8'))