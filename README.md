Welcome!  If you've stumbled here and notice something wrong please open an issue or PR.  Much to learn in ML and Python I still have.  Thanks!

# MLDemos


## Project 1:

### Housing classification - Descision Tree

Tutorial: http://www.r2d3.us/visual-intro-to-machine-learning-part-1/

Dataset: https://github.com/jadeyee/r2d3-part-1-data/blob/master/part_1_data.csv


## Project 2:

### MNIST example in Keras - CNN

https://github.com/fbomb111/MLDemos/blob/master/MNISTInKeras/MNIST%20in%20Keras.ipynb

A detailed look into CNN's with Keras and final output to Apple's CoreML `.mlmodel`

## Project 3:

### AWSComprehend

https://github.com/fbomb111/MLDemos/tree/master/AWSComprehend

Both a python notebook and iOS application to give a quick and simple sentiment analysis based on user-entered text using AWSComprehend


## Converters (object detection)


### [OIDV4ToCreateMLJSONConverter.py](https://github.com/fbomb111/MLDemos/blob/master/Converters/OIDV4ToCreateMLJSONConverter.py)

Converts from [Google's Open Images Database](https://storage.googleapis.com/openimages/web/index.html), using the [OIDV4 tool](https://github.com/EscVM/OIDv4_ToolKit)), to a JSON format that can be used with [Apple's Create ML Object Detector](https://developer.apple.com/documentation/createml/mlobjectdetector/datasource).

### [SimpleAnnotatorCSVToCreateMLJSONConverter.py](https://github.com/fbomb111/MLDemos/blob/master/Converters/SimpleAnnotatorCSVToCreateMLJSONConverter.py)

Converts the CSV output from the [Simple Annotator Tool](https://github.com/sgp715/simple_image_annotator), to a JSON format that can be used with [Apple's Create ML Object Detector](https://developer.apple.com/documentation/createml/mlobjectdetector/datasource).

### [SimpleAnnotatorCSVToRecordIOLST.py](https://github.com/fbomb111/MLDemos/blob/master/Converters/SimpleAnnotatorCSVToRecordIOLST.py)

Converts the CSV output from the [Simple Annotator Tool](https://github.com/sgp715/simple_image_annotator), to the LST format required before conversion to REC format. [MXNet format details here](https://mxnet.apache.org/api/python/image/image.html#image-iterator-for-object-detection). 

More to come when I get this working with [AWS SageMaker Object Detection Algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection.html)
