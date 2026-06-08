# import required libraries
from  Database.Tables.Tables import *
from CNN.Models import ModelFactory
import random

# trains the one architecture or version according the requirements of the user.
# by architecture is meant to be the type of model, for example ResNet, VGG, etc. and by version is meant an specific set of hyperparameters or combination
# of training-, testing-, and validation datasets.
# Trains only one architecture or version of an architecture at a time.
def trainModel(clientAnswer:dict)->None:

    # fetches the model names from the database
    modelNames=ModelTable("your_database.db")
    
    # checks if the model already exists in the database
    if clientAnswer.get('ModelName') in modelNames.fetchInfo(statement="SELECT ModelName FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName'))):

        # checks if the model version already exists in the database
        modelVersion=ModelVersionTable("your_database.db") # gets the table of model versions

        if clientAnswer.get('ModelVersion') in modelVersion.fetchInfo(statement="SELECT ModelVersion FROM ModelVersion WHERE ModelVersion={}".format(clientAnswer.get('ModelVersion'))):

            # informs the user that the model version already exists and does not proceed with the training
            print("The model version already exists in the database. Please choose another name or update the existing model version.")

            # returns None
            return None
        
        # if the model version does not exist, proceeds with the creation of the model and the training
        else:

            # creates an instance of the model to be trained
            modelToBeTrained=ModelFactory().createModel(modelName=clientAnswer.get('ModelName'), numClasses=clientAnswer.get('NumClasses'))

            

            modelToBeTrained.trainModel(
                trainDataset=clientAnswer.get('TrainDataset'),
                validationDataset=clientAnswer.get('ValidationDataset'),
                epochs=clientAnswer.get('Epochs'),
                checkPoint=clientAnswer.get('CheckPoint')
            ) # number of classes to be defined by the user and it will be fixed for this project

            # gets the model ID of the model name given by the user
            modelID=modelNames.fetchInfo(statement="SELECT ModelID FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName')))

            # inserts a model version to the database
            modelVersion.insertModelVersionTable()



    if clientAnswer.get('ModelName') in ModelTable("your_database.db").fetchInfo(statement="SELECT ModelName FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName'))):

        # informs the user that the model already exists and does not proceed with the training
        print("The model already exists in the database. Please choose another name or update the existing model.")

        return None
    
    
    
    # First:
    # The dataset is divided into training, testing, and validation datasets acording the structure of the data management system.
    # The type of architecture is defined together with its hyperparameters.

    # creates an instance of the table TFRecording
    Table=TFRecordingTable()

    # fetches the whole table TFrecoridng 
    recordings=Table.fetchTFRecording()

    # loops through and checks the label. 
    # takes the labels and divide them into their original segments
    # takes the second and third item of every recording. The third is converted into an integral
    # these are stored in a list and sampled randomly for validation, testing, a training dataset formation#

    # initializes the list of sampleNameInt
    sampleNameIntList=[]

    # initializes the list of material types
    materialTypeList=[]

    for record in recordings:

        # gets the content of the category label of the record in recordings
        label=record.get('Label')

        # takes the label content and divides it into name segments
        labelSegments=label.split("_")

        # gets the material type of the sample and the sample number
        materiaType=labelSegments[1]
        sampleNumber=int(labelSegments[2])

        # appends the sampleNameInt and the material type to their respective lists
        sampleNameIntList.append(sampleNumber)
        materialTypeList.append(materiaType)

    # converst the validation, testing, and training percentages given by the user into the number of samples for each dataset
    validationSamplesNumber=int((clientAnswer.get('ValidationPercentage')/100)*len(sampleNameIntList))
    testingSamplesNumber=int((clientAnswer.get('TestingPercentage')/100)*len(sampleNameIntList))
    trainingSamplesNumber=int((clientAnswer.get('TrainingPercentage')/100)*len(sampleNameIntList))

    # gets the identification of the samples for the training, validation, and testing datasets according to the percentages given by the user
    validationSamples=random.sample(sampleNameIntList, k=validationSamplesNumber)
    testingSamples=random.sample([x for x in sampleNameIntList if x not in validationSamples], k=testingSamplesNumber)
    trainingSamples=[x for x in sampleNameIntList if x not in validationSamples and x not in testingSamples]

    # store the sampleNameInt in a list for the sampling of the datasets
    #HSU-HH_K_001

    if clientAnswer.get('')

    # Second:
    # Checks if the version of the architecture exists in the database
    # If it exists, informs about it and does not proceed with the training
    # If it does not exist, proceeds with the training #

    # Third: 
    # Updates the database tables accordingly#
    
    return None

# defines the fuction to train several models
def trainSeveralModels()->None:

    # First:
    # The dataset is divided into training, testing, and validation datasets acording the structure of the data management system.
    # The types of architectures are defined together with their hyperparameters.

    # Second:
    # Checks if the versions of the architectures exist in the database
    # If they exist, informs about it and does not proceed with the training
    # If they do not exist, proceeds with the training #

    # Third: 
    # Updates the database tables accordingly#

    return None

# defines the fuction to train all the models
def trainAllModels()->None:

    # First:
    # The dataset is divided into training, testing, and validation datasets acording the structure of the data management system.
    # The types of architectures are defined together with their hyperparameters.

    # Second:
    # Checks if the versions of the architectures exist in the database
    # If they exist, informs about it and does not proceed with the training
    # If they do not exist, proceeds with the training #

    # Third:
    # Updates the database tables accordingly#

    return None
