#!/usr/bin/python
import argparse
import turicreate as tc
from turicreate import SFrame

__author__ = 'Frankie Cleary'
 
parser = argparse.ArgumentParser(description='Input should be CSV. The output will be JSON')
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()
 
## show values ##
print ("Input file: %s" % args.input )
print ("Output file: %s" % args.output )

def row_to_bbox_coordinates(row):
    """
    Takes a row and returns a dictionary representing bounding
    box coordinates:  (center_x, center_y, width, height)  e.g. {'x': 100, 'y': 120, 'width': 80, 'height': 120}
    """
    return {'x': row['xMin'] + (row['xMax'] - row['xMin'])/2, 
            'y': row['yMin'] + (row['yMax'] - row['yMin'])/2, 
            'width': (row['xMax'] - row['xMin']),
            'height': (row['yMax'] - row['yMin'])}

sf = SFrame.read_csv(args.input)

# rename columns to the input required for create ml
sf = sf.rename({'name': 'label', 'image': 'imagefilename'})

# convert coordinates system to origin and size
sf['coordinates'] = sf.apply(row_to_bbox_coordinates)

# delete unused columns
del sf['xMin'], sf['xMax'], sf['yMin'], sf['yMax'], sf['id']

# nest columns into a new column
sf = sf.pack_columns(['label', 'coordinates'], new_column_name='bbox', dtype=dict)

# make filenames unique via groupby
sf = sf.groupby('imagefilename', {'annotation': tc.aggregate.CONCAT('bbox')})

sf.export_json(args.output + '.json', orient='records')
