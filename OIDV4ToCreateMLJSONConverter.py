#!/usr/bin/python
import argparse
from functools import reduce
import turicreate as tc
from turicreate import SFrame
import os
import boto3
from s3fs.core import S3FileSystem

__author__ = 'Frankie Cleary'
 
parser = argparse.ArgumentParser(description='The output will be JSON')
parser.add_argument('-i','--images', help='Path to images folder',required=True)
parser.add_argument('-l','--labels', help='Path to labels folder',required=True)
parser.add_argument('-o','--output',help='Output file prefix name', required=True)
args = parser.parse_args()
 
## show values ##
print ("Images path: %s" % args.images )
print ("Labels path: %s" % args.labels )
print ("Output file: %s" % args.output )

def createFrame(file):
    frame = SFrame.read_csv(args.labels + '/' + file, delimiter=' ', header=False)
    frame = frame.rename({'X1': 'name', 'X2':'xMin', 'X3':'yMin', 'X4':'xMax', 'X5':'yMax'})
    frame['image'] = os.path.splitext(file)[0]
    return frame

# labels = list(filter(os.path.isfile, os.listdir( args.labels ) ) )
labels = os.listdir(args.labels)

if '.DS_Store' in labels:
	labels.remove('.DS_Store')

frames = [createFrame(file) for file in labels]
sf = reduce((lambda x, y: x.append(y)), frames)

def row_to_bbox_coordinates(row):
    """
    Takes a row and returns a dictionary representing bounding
    box coordinates:  (center_x, center_y, width, height)  e.g. {'x': 100, 'y': 120, 'width': 80, 'height': 120}
    """
    return {'x': row['xMin'] + (row['xMax'] - row['xMin'])/2, 
            'y': row['yMin'] + (row['yMax'] - row['yMin'])/2, 
            'width': (row['xMax'] - row['xMin']),
            'height': (row['yMax'] - row['yMin'])}

# rename columns to the input required for create ml
sf = sf.rename({'name': 'label', 'image': 'imagefilename'})

# convert coordinates system to origin and size
sf['coordinates'] = sf.apply(row_to_bbox_coordinates)

# delete unused columns
del sf['xMin'], sf['xMax'], sf['yMin'], sf['yMax']

# nest columns into a new column
sf = sf.pack_columns(['label', 'coordinates'], new_column_name='bbox', dtype=dict)

# make filenames unique via groupby
sf = sf.groupby('imagefilename', {'annotation': tc.aggregate.CONCAT('bbox')})

sf.export_json(args.output + '.json', orient='records')
