#!/usr/bin/python
import argparse
import mxnet as mx #requires mxnet==1.2.1
import subprocess
import os

__author__ = 'Frankie Cleary'

parser = argparse.ArgumentParser(description='Input should be CSV. The output will be JSON')
parser.add_argument('-i','--input', help='Input folder name',required=True)
parser.add_argument('-o','--output',help='Output file prefix name', required=True)
args = parser.parse_args()

im2rec_path = mx.test_utils.get_im2rec_path()
data_path = args.input
output_prefix = args.output

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['python', im2rec_path, '--list', '--recursive', '--test-ratio=0.2', '--train-ratio=0.8', output_prefix, data_path], stdout=devnull)

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['python', im2rec_path, '--num-thread=4', '--pass-through', output_prefix + '_train', data_path], stdout=devnull)
    subprocess.check_call(['python', im2rec_path, '--num-thread=4', '--pass-through', output_prefix + '_test', data_path], stdout=devnull)