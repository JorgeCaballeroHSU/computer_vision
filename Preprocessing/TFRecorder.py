# this class is used to record and read images in and from tfrecord format

# import required libraries
import tensorflow as tf
import os

# define the TFRecorder class
class TFRecorder:
    def __init__(self, tfrecordDir: str):
        self.tfrecordDir = tfrecordDir

    def __floatFeature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))
    
    def __int64Feature(*value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))
    
    def __stringFeature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value.encode('utf-8')]))

    # module for the creation of TFrecord files
    def createTFRecord(self, fileName: str, label: str, labelInit: int)-> bytes:
        ''''creates a TFRecord file from an image file name, label, and labelInit and returns the serialized TFRecord
        Args:
            fileName: the file name of the image to be recorded
            label: the label of the image to be recorded
            labelInit: the initial label of the image to be recorded
        Returns:
            the serialized TFRecord of the image, label, and labelInit
        '''

        # calls the module read and decode for the reading and decoding of the images and labels
        image=self.readAndDecode(fileName  = fileName)
            
        # gets the dimensions of the image
        imageShape = image.shape

        # flatten the image to 1D array
        image = tf.reshape(image, [-1])

        # returns serialized image and label
        return tf.train.Example(features=tf.train.Features(feature={
            'image': self.__floatFeature(image),
            'shape': self.__int64Feature(imageShape[0], imageShape[1], imageShape[2]),
            'label': self.__stringFeature(label),
            'label_init': self.__int64Feature(labelInit)
        })).SerializeToString() 

    
    #creates the module for for reading and decoding the images and labels
    def readAndDecode(self, fileName: str)-> tf.Tensor:
        '''reads and decodes an image from a file name and returns a tensor
        Args:
            fileName: the file name of the image to be read and decoded
        Returns:
            the decoded image tensor
        '''

        # reads the image from the file name
        image = tf.io.read_file(fileName)   

        # decodes the image to a tensor
        image = tf.image.decode_jpeg(image, channels=3)

        # normalizes the image to the range [-1, 1]
        image = tf.cast(image, tf.float32) / 255.0 - 0.5

        # returns the image tensor
        return image
    
    # module for the reading of TensorFlow records
    def readTFRecord(self, fileName: str)-> tf.data.Dataset:
        '''reads a TFRecord file and returns a dataset of images, labels, and labelInit
        Args:
            fileName: the file name of the TFRecord to be read
        Returns:
            a dataset of images, labels, and labelInit
        '''

        # creates a dataset from the TFRecord file
        dataset = tf.data.TFRecordDataset(fileName)

        # defines the feature description for parsing the TFRecord
        featureDescription = {
            'image': tf.io.VarLenFeature(tf.float32),
            'shape': tf.io.FixedLenFeature(tf.int64),
            'label': tf.io.FixedLenFeature([], tf.string, default_value=''),
            'label_init': tf.io.FixedLenFeature([], tf.int64, default_value=0)
        }

        # parses the TFRecord and returns the dataset
        rec=tf.io.parse_single_example(fileName, featureDescription)

        # gets the image, label, and labelInit from the parsed record
        shape = rec['shape']
        image = tf.sparse.to_dense(rec['image'],shape=shape)
        label = rec['label']
        labelInit = rec['label_init']

        # returns the image, label, and labelInit
        return image, label, labelInit
    
    # saves the TFRecord in the indicated location
    def saveTFRecord(self,fileName:str,filePath:str, TFRecord:bytes)->None:

        # creates the file location where the TF record is to be saved
        storeLocation=r'/'.join(filePath,fileName)

        # saves file in the indicated location
        with open(file=storeLocation, mode='a') as file:
            
            # creates and writes the file in the indicated location
            file.write(TFRecord)

            # closes the file 
            file.close()

        # returns None
        return None


        

    

