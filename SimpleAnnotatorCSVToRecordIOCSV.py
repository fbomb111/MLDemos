#!/usr/bin/python
import argparse
import pandas as pd
from sklearn import preprocessing

__author__ = 'Frankie Cleary'

parser = argparse.ArgumentParser(description='Input should be CSV. The output will be CSV')
parser.add_argument('-i','--input', help='Input folder name',required=True)
parser.add_argument('-o','--output',help='Output file prefix name', required=True)
args = parser.parse_args()

# read the file
df = pd.read_csv(args.input)

# change label to numeric category
le = preprocessing.LabelEncoder()
le.fit(df['name'])
df['name'] = le.transform(df['name']) 

# drop unecessary columns
df = df.drop('id', axis=1)

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
allDF.insert(0, 'headerWidth', '2')
allDF.insert(1, 'objectWidth', numOfColumns)

allDF.to_csv(args.output + '.csv')