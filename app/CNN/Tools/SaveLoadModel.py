# module for saving the trained model

# imports required libraries
import os
import tensorflow as tf

# defines the SaveModel class for saving the trained model
class SaveModel:

    # space for the properties of the class
    __pathFile:str=''

    # module for the initialization of the class
    def __init__(self, model: tf.keras.Model, saveDir: str, fileName: str)-> None:
        
        # initializes the properties of the class
        self.model = model
        self.saveDir = saveDir
        self.fileName = fileName

        # creates the file path for saving the model
        self.__createFilePath()

        #returns nothing
        return None

    # module for the creation of the file path for saving the model
    def __createFilePath(self)-> None:
        '''creates a file path for saving the model and returns the file path'''
        self.__pathFile = os.path.join(self.saveDir, self.fileName)

    # module for saving the trained model
    def saveModel(self)-> None:
        '''saves the trained model to the specified directory'''

        # saves the model to the specified directory
        self.model.save(self.__pathFile)

        # returns nothing
        return None
    
# module for loading a saved model
class LoadModel:
    
    # space for the properties of the class
    __pathFile:str=''

    # module for the initialization of the class
    def __init__(self, saveDir: str, fileName: str)-> None:
        
        # initializes the properties of the class
        self.saveDir = saveDir
        self.fileName = fileName

        # creates the file path for loading the model
        self.__createFilePath()

        # returns nothing
        return None

    # module for the creation of the file path for loading the model
    def __createFilePath(self)-> None:
        '''creates a file path for loading the model and returns the file path'''
        self.__pathFile = os.path.join(self.saveDir, self.fileName)

    # module for loading a saved model
    def loadModel(self)-> tf.keras.Model:
        '''loads a saved model from the specified directory and returns the loaded model'''

        # loads the model from the specified directory
        model = tf.keras.models.load_model(self.__pathFile)

        # returns the loaded model
        return model