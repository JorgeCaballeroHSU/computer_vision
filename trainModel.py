# import required libraries
import keras
from datetime import datetime

from  Database.Tables.Tables import *
from CNN.Models import ModelFactory
import random

# Samples the dataset for training and validation dataset formation according to the percentages given by the user in the frontend
def datasetSampling(clientAnswer:dict)->list[list,list]:

    # gets the sampleNameIntList from the database
    sampleNameIntList=TFRecordingTable("your_database.db").fetchInfo(statement="SELECT FilePath FROM TFRecording")

    # converst the percentages given by the user into numbers of samples for the training and validation datasets
    validationSamplesNumber=int((clientAnswer.get('ValidationPercentage')/100)*len(sampleNameIntList))
    trainingSamplesNumber=int((clientAnswer.get('TrainingPercentage')/100)*len(sampleNameIntList))

    # gets the identification of the samples for the training, validation, and testing datasets according to the percentages given by the user
    validationSamples=random.sample(sampleNameIntList, k=validationSamplesNumber)
    trainingSamples=random.sample([x for x in sampleNameIntList if x not in validationSamples], k=trainingSamplesNumber)
    
    # returns the training and validation samples
    return [trainingSamples, validationSamples]


# trains the one architecture or version according the requirements of the user.
# by architecture is meant to be the type of model, for example ResNet, VGG, etc. and by version is meant an specific set of hyperparameters or combination
# of training-, testing-, and validation datasets.
# Trains only one architecture or version of an architecture at a time.
def trainModel(clientAnswer:dict)->None|list[dict]:

    # fetches the model names from the database
    modelNames=ModelTable("your_database.db")
    
    # checks if the model already exists in the database
    # if the model alreay exists in the database#
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

            # samples the dataset for training and validation dataset formation according to the percentages given by the user in the frontend
            sampledDatasets=datasetSampling(clientAnswer=clientAnswer)
            
            # gets the last version of the model with the same name from the database
            newModelVersion=modelVersion.fetchInfo(statement="SELECT MAX(ModelVersion) FROM ModelVersion WHERE ModelID={}".format(modelNames.fetchInfo(statement="SELECT ModelID FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName')))))
            newModelVersion=newModelVersion[0]['MAX(ModelVersion)']+1 if newModelVersion[0]['MAX(ModelVersion)'] is not None else 1

            # defines the filepath for saving the best model during training
            filePath='{}_version_{}'.format(clientAnswer.get('ModelName'), newModelVersion)

            # defines the checkpoint for saving the best model during training
            checkPoint=keras.callbacks.ModelCheckpoint(
                filepath=filePath, 
                monitor='val_loss', 
                save_best_only=True)
            
            # trains the model with the training dataset and validates it with the validation dataset for a 
            # specified number of epochs and saves the best model using the specified checkpoint
            # gets the history#
            history=modelToBeTrained.trainModel(
                trainDataset=sampledDatasets[0], # contains the train samples
                validationDataset=sampledDatasets[1], # contains the validation samples
                epochs=clientAnswer.get('Epochs'),
                checkpoint=checkPoint
            ) 

            # updates the table ModelWeights and gets the last ID
            lastArrowIDModelWeightsTable=ModelWeightsTable(dbFile="your_database.db").insertModelWeightsTable(
                clientAnswer={'ModelWeightsPath':filePath})
            
            # updates the table Hyperparameters and gets the last ID
            lastArrowIDHyperparametersTable=HyperparameterTable(dbFile="your_database.db").insertHyperparameterTable(
                clientAnswer={'Hyperparameters':clientAnswer.get('Hyperparameters')})
            
            # updates the table Model Metrics and gets the last ID
            lastArrowModelMetricTable=ModelMetricTable(dbFile="your_database.db").insertModelMetricTable(
                clientAnswer={'MSE':history.get('mse'), 'r2':history.get('accuracy'), 'loss':history.get('loss')})
            
            # updates the table ModelVersion and gets the last ID
            lastArrowModelVersion=ModelVersionTable(dbFile="your_database.db").insertModelVersionTable(
                clientAnswer={
                    'ModelVersion':newModelVersion,
                    'CreatedAt':datetime.isoformat(),
                    'ModelMetricID':lastArrowModelMetricTable,
                    'HyperparameterID':lastArrowIDHyperparametersTable,
                    'ModelWeights':lastArrowIDModelWeightsTable
                })
            
            # updates the table Model and gets the last ID ´
            LastArrowModelTable=ModelTable(dbFile="your_database.db").fetchInfo(statement="SELECT ModelID FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName')))[0]
            
            # creates an instace of Validation, Training, and TFRecord table to insert data in the tables
            validationTable=ValidationTable(dbFile="your_database.db")
            trainingTable=TrainingTable(dbFile="your_database.db")
            TFRecordTable=TFRecordingTable(dbFile="your_database.db")

            # updates the table validation
            for sample in sampledDatasets[0]:
                validationTable.insertValidationTable(
                    clientAnswer={
                        'TFRecordingID':TFRecordTable.fetchInfo(statement='SELECT TFRecordingID FROM TABLE TFRecord WHERE Label={}'.format(sample))[0],
                        'ModelID':LastArrowModelTable
                    }
                    )

            # updates the table training
            for sample in sampledDatasets[1]:
                trainingTable.insertValidationTable(
                    clientAnswer={
                        'TFRecordingID':TFRecordTable.fetchInfo(statement='SELECT TFRecordingID FROM TABLE TFRecord WHERE Label={}'.format(sample))[0],
                        'ModelID':LastArrowModelTable
                    }
                    )
            
            # returns the new stetate of the database to show in the webpage
            return [
                validationTable.fetchValidation(),
                trainingTable.fetchTraining(),
                ModelVersionTable(dbFile="your_database.db").fetchModelVersion(),
                ModelMetricTable(dbFile="your_database.db").fetchModelMetric(),
                ModelWeightsTable(dbFile="your_database.db").fetchModelWeights(),
                ModelTable(dbFile="your_database.db").fetchModel(),
                HyperparameterTable(dbFile="your_database.db").fetchHyperparameter()
            ]

    # if the model does not exist in the database
    else:

        # informs the user tha the model does not exist in the database and a new one will be created.
        print("The model was not found in the database. A new model will be added to the database.")

        # creates an instance of the model to be trained
        modelToBeTrained=ModelFactory().createModel(modelName=clientAnswer.get('ModelName'), numClasses=clientAnswer.get('NumClasses'))

        # samples the dataset for training and validation dataset formation according to the percentages given by the user in the frontend
        sampledDatasets=datasetSampling(clientAnswer=clientAnswer)
        
        # gets the last version of the model with the same name from the database
        newModelVersion=modelVersion.fetchInfo(statement="SELECT MAX(ModelVersion) FROM ModelVersion WHERE ModelID={}".format(modelNames.fetchInfo(statement="SELECT ModelID FROM Model WHERE ModelName={}".format(clientAnswer.get('ModelName')))))
        newModelVersion=newModelVersion[0]['MAX(ModelVersion)']+1 if newModelVersion[0]['MAX(ModelVersion)'] is not None else 1

        # defines the filepath for saving the best model during training
        filePath='{}_version_{}'.format(clientAnswer.get('ModelName'), newModelVersion)

        # defines the checkpoint for saving the best model during training
        checkPoint=keras.callbacks.ModelCheckpoint(
            filepath=filePath, 
            monitor='val_loss', 
            save_best_only=True)
        
        # trains the model with the training dataset and validates it with the validation dataset for a 
        # specified number of epochs and saves the best model using the specified checkpoint
        # gets the history#
        history=modelToBeTrained.trainModel(
            trainDataset=sampledDatasets[0], # contains the train samples
            validationDataset=sampledDatasets[1], # contains the validation samples
            epochs=clientAnswer.get('Epochs'),
            checkpoint=checkPoint
        ) 

        # updates the table ModelWeights and gets the last ID
        lastArrowIDModelWeightsTable=ModelWeightsTable(dbFile="your_database.db").insertModelWeightsTable(
            clientAnswer={'ModelWeightsPath':filePath})
        
        # updates the table Hyperparameters and gets the last ID
        lastArrowIDHyperparametersTable=HyperparameterTable(dbFile="your_database.db").insertHyperparameterTable(
            clientAnswer={'Hyperparameters':clientAnswer.get('Hyperparameters')})
        
        # updates the table Model Metrics and gets the last ID
        lastArrowModelMetricTable=ModelMetricTable(dbFile="your_database.db").insertModelMetricTable(
            clientAnswer={'MSE':history.get('mse'), 'r2':history.get('accuracy'), 'loss':history.get('loss')})
        
        # updates the table ModelVersion and gets the last ID
        lastArrowModelVersion=ModelVersionTable(dbFile="your_database.db").insertModelVersionTable(
            clientAnswer={
                'ModelVersion':newModelVersion,
                'CreatedAt':datetime.isoformat(),
                'ModelMetricID':lastArrowModelMetricTable,
                'HyperparameterID':lastArrowIDHyperparametersTable,
                'ModelWeights':lastArrowIDModelWeightsTable
            })
        
        # updates the table Model and gets the last ID ´
        LastArrowModelTable=ModelTable(dbFile="your_database.db").insertItemsTable(
            clientAnswer={'ModelName':clientAnswer.get('ModelName'),
                            'TrainingStatus':'Finalized',
                            'CreatedAt':datetime.isoformat(),
                            'ModelVersionID':lastArrowModelVersion})
        
        # creates an instace of Validation, Training, and TFRecord table to insert data in the tables
        validationTable=ValidationTable(dbFile="your_database.db")
        trainingTable=TrainingTable(dbFile="your_database.db")
        TFRecordTable=TFRecordingTable(dbFile="your_database.db")

        # updates the table validation
        for sample in sampledDatasets[0]:
            validationTable.insertValidationTable(
                clientAnswer={
                    'TFRecordingID':TFRecordTable.fetchInfo(statement='SELECT TFRecordingID FROM TABLE TFRecord WHERE Label={}'.format(sample))[0],
                    'ModelID':LastArrowModelTable
                }
                )

        # updates the table training
        for sample in sampledDatasets[1]:
            trainingTable.insertValidationTable(
                clientAnswer={
                    'TFRecordingID':TFRecordTable.fetchInfo(statement='SELECT TFRecordingID FROM TABLE TFRecord WHERE Label={}'.format(sample))[0],
                    'ModelID':LastArrowModelTable
                }
                )
        
        # returns the new stetate of the database to show in the webpage
        return [
            validationTable.fetchValidation(),
            trainingTable.fetchTraining(),
            ModelVersionTable(dbFile="your_database.db").fetchModelVersion(),
            ModelMetricTable(dbFile="your_database.db").fetchModelMetric(),
            ModelWeightsTable(dbFile="your_database.db").fetchModelWeights(),
            ModelTable(dbFile="your_database.db").fetchModel(),
            HyperparameterTable(dbFile="your_database.db").fetchHyperparameter()
        ]

  
# defines the fuction to train several models
def trainSeveralModels(clientAnswer:list[dict])->list[dict]:

   # loops through the list of dictionaries to train the models in the list
   for answer in clientAnswer:

    # trains a model at the time
    results=trainModel(clientAnswer=answer)

    # returns last results
    return results

# defines the fuction to train all the models
def trainAllModels(clientAnswer:dict)->None:

    # gets the name of all the available models
    modelNames=ModelTable(dbFile="your_database.db").fetchInfo(statement="FROM Model SELECT ModelName")

    # loops through all the models available and execute the function train model
    for name in modelNames[0]:

        # adds the ModelName key to dictionary
        clientAnswer['ModelName']=name.get['ModelName']

        # executes the function train model and get the results
        results=trainModel(clientAnswer=clientAnswer)
    
    # returns the last results
    return results
