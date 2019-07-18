#!/usr/bin/python
import argparse
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import os
import cv2

__author__ = 'Frankie Cleary'

parser = argparse.ArgumentParser(description='Input should be CSV. The output will be CSV')
parser.add_argument('-c','--csv', help='Input csv name',required=True)
parser.add_argument('-i','--images', help='Input images path',required=True)
parser.add_argument('-o','--output',help='Output file prefix name', required=True)
args = parser.parse_args()

def sizeForImage(df):
    
    # read image
    img = cv2.imread(args.images + '/' + df['image'], cv2.IMREAD_UNCHANGED)

    # get dimensions of image
    dimensions = img.shape
 
    # height, width, number of channels in image
    df['height'] = img.shape[0]
    df['width'] = img.shape[1]
    return df

# read the file
df = pd.read_csv(args.csv)

# add image size to data frame
df = df.apply(sizeForImage, axis=1)

# convert bbox to 1.0 scale
df['xMin'] = df['xMin'] / df['width']
df['xMax'] = df['xMax'] / df['width']
df['yMin'] = df['yMin'] / df['height']
df['yMax'] = df['yMax'] / df['height']

# change label to numeric category
le = preprocessing.LabelEncoder()
le.fit(df['name'])
df['name'] = le.transform(df['name']) 

# drop unecessary columns
df = df.drop('id', axis=1)

# keep track of image size but drop it from main data frame
sizeDF = df[['image','height', 'width']]
sizeDF = sizeDF.drop_duplicates(keep='first')
sizeDF = sizeDF.set_index('image')
df = df.drop('height', axis=1)
df = df.drop('width', axis=1)

# groupby image and unstack
df = df.set_index(['image', df.groupby('image').cumcount()]).unstack()
numOfColumns = len(df.columns.levels[0])
numOfSubColumns = len(df.columns.levels[1])

# rearrange the columns so you have the first row of each sublevel, then second, and so on
allDF = df.xs(0, axis=1, level=1)

for index in range(1, numOfSubColumns):
    level = df.columns.levels[1][index]
    subDF = df.xs(level, axis=1, level=1)
    allDF = allDF.merge(subDF, on='image', how='inner', suffixes=('_' + str(index), '_' + str(index + 1)))

# insert the object data
df = allDF
df.insert(0, 'headerWidth', '4')
df.insert(1, 'objectWidth', numOfColumns)
df.insert(2, 'height', sizeDF['height'])
df.insert(3, 'width', sizeDF['width'])

df = df.rename_axis('image').reset_index()

# send image column to the end
order = df.columns.tolist()[1:] + ['image']
df = df[order]

# remove all blanks from the data frame
df = pd.DataFrame(df.apply(lambda x : sorted(x,key=pd.isnull),1).tolist()).fillna('')

# split into 80/20 train/test and export as .lst
train, test = train_test_split(df, test_size=0.2)
train.to_csv(args.output + '_train' + '.lst', sep='\t', float_format='%.4f', header=None)
test.to_csv(args.output + '_test' + '.lst', sep='\t', float_format='%.4f', header=None)