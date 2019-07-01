#!/usr/bin/python
import argparse
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

__author__ = 'Frankie Cleary'

parser = argparse.ArgumentParser(description='Input should be CSV. The output will be CSV')
parser.add_argument('-i','--input', help='Input csv name',required=True)
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
df = allDF
df.insert(0, 'headerWidth', '2')
df.insert(1, 'objectWidth', numOfColumns)

df = df.rename_axis('image').reset_index()

# send image column to the end
order = df.columns.tolist()[1:] + ['image']
df = df[order]

# fill all blanks with 0 
df = df.fillna(0)

# split into 80/20 train/test and export as .lst
train, test = train_test_split(df, test_size=0.2)
train.to_csv(args.output + '_train' + '.lst', sep='\t', float_format='%.4f', header=None)
test.to_csv(args.output + '_test' + '.lst', sep='\t', float_format='%.4f', header=None)