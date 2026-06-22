# class for the creation of a checkpoint for saving the model during training
# imports required libraries
import os
import tensorflow as tf

# defines the CheckPoint class for the creation of a checkpoint for saving the model during training
class CheckPoint:
    
    # space for the properties of the class
    __pathFile:str=''

    # module for the initialization of the class
    def __init__(self, saveDir: str, fileName: str)-> None:
        
        # initializes the properties of the class
        self.saveDir = saveDir
        self.fileName = fileName

        # creates the file path for saving the model
        self.__createFilePath()

        # returns nothing
        return None

    # module for the creation of the file path for saving the model
    def __createFilePath(self)-> None:
        '''creates a file path for saving the model and returns the file path'''
        self.__pathFile = os.path.join(self.saveDir, self.fileName)

    # module for creating a checkpoint for saving the model during training
    def createCheckPoint(self)-> tf.keras.callbacks.ModelCheckpoint:
        '''creates a checkpoint for saving the model during training and returns the checkpoint'''
        checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=self.__pathFile, save_weights_only=False, save_best_only=True, monitor='val_accuracy', mode='max')

        return checkpoint