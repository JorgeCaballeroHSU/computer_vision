#imports required libraries
from importlib.resources import path

from Tools.ChangePath import ChangePath
from Tools.Format import addDataType
from app.Files.Path import Path
from app.Files.Label import LabelPreprocessing, LabelSample
from app.Database.Tables.Tables import *
from app.Preprocessing.TFRecorder import TFRecorder
import os
import numpy as np

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()


# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(clientAnswer:dict, action:str, image:str)->dict:
    
    # gets the image from the client
    # It assumes that the client will send the image as chucks that will be put together at the socket class
    # it assumes that the picture will be received as binary that will be decoded at the socket class  

    # creates the object label from class LabelSample
    label=LabelSample()

    # creates the object path from the class Path
    path=Path()

    # stores the file in the indicated address if the action is to "add" a new sample
    if action=='add':
        
        # stores the image in the defined path
        # sets the path to save the files
        path.setPath(path=pathFormat.changePathWindowsToWsl(path=windowsAddress))

        # generates label for the picture
        label.setLabelType(labelType=clientAnswer.get('labelType')) # sets the label type
        labelFile=label.generateSampleLabel()

        # creates a file where the image is going to be saved
        with open(
            file=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')),
            mode='wb'
            ) as f:

            # saves the file
            f.write(image) #-> client answer contains the image as binary

            # closes the file when is over
            f.close()

        # generates the dict of data to add an item to the sample table
        clientDataset={
            'Label':labelFile,
            'FilePath':path.getPath(),
            'CaptureTime':clientAnswer['CaptureTime'],
            'CameraID':clientAnswer['CameraID'],
            'DatasetID':clientAnswer['DatasetID'],
            'MaterialID':clientAnswer['MaterialID']
        }

        # updates the sample table
        return Sample(clientDataset=clientDataset, table=SampleTable, action=action )
    
    # if the action is to delete a sample, then the file has to be deleted from the hard drive and the register from the database
    elif action=='delete':
        
        # generates the file path
        pathFile='{}/{}.jpeg'.format(clientAnswer['FilePath'],clientAnswer['Label'])

        # deletes the file in the hard drive
        try:
            os.remove(path=pathFile) #### ----> it has to be added handling of errors
            
            #returns results from the deletion of the database
            return Sample(clientDataset=clientAnswer,table=SampleTable,action=action)
        except OSError as e:

            # prints error
            print('An error has accurred: {}'.format(e))

            # indicates that the file cannot be deleted
            print('File cannot be removed')
    
    # if the something in the database wants to be modified
    elif action=='modify':

        # returns results from table Sample modification
        return Sample(clientDataset=clientAnswer,table=SampleTable,action=action)
        

# gets the pcitures into a TensorFlow record format for later use in the training of the model
def generateTensorFlowRecords(path:Path, database:Database, tfRecorder:TFRecorder, labelFile:str)->None:

    #creates a TensorFlow record

    # gets the file path of the file
    filePath=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg'))

    # creates the TF record with the file path, the label and the labelInit
    record=tfRecorder.createTFRecord(
        fileName=filePath,
        label=labelFile,
        labelInit=database.fetchInfo(query='''SELECT LabelID FROM label WHERE name=?''', values=(labelFile, 
        ))[0]['LabelID'])
    
    # saves the TF record in the indicated location
    tfRecorder.saveTFRecord(
        fileName=''.join(labelFile,'tfrec'),
        filePath=path.getPath(),
        TFRecord=record
    )

    # updates the table TFrecording the binary of the TF record.
    database.insertItemsTable(
        query='''INSERT INTO TFRecording (name, label, labelInit, filePath) VALUES (?, ?, ?, ?) ''',
        values=(labelFile, labelFile, database.fetchInfo(query='''SELECT LabelID FROM label WHERE name=?''', values=(labelFile, 
        ))[0]['LabelID'], ''.join(path.getPath(),addDataType(fileName=labelFile,dataType='tfrec')))
    )


# imports required libraries
from app.Preprocessing import Tailing

# Preprocesses the images by applying tailing
def PreprocessingImages(clientAnswer:dict)->list:

    # creates a Tailing object to extract image patches from the picture
    tailing=Tailing(size=512,stride=512) #--> the size 512 is used to be able to maintain the details of the image and train the model with a good amount of details

    # creates a getPath object to get the path where the images are located
    path=Path()

    # gets the path where the images are located
    fotosPath=path.getPath()

    # creates an LabelPreprocessing object to generate the labels for the preprocessed files
    labelPreprocessing=LabelPreprocessing(sampleLabel='',preprocessingType='tailing')

    # gets a list of files avialables in the path
    filesAvailable=os.listdir(path=fotosPath)

    # loops through every file available
    for file in filesAvailable:
        
        # generates the address of the file and opens it for use read only.
        photoLocation= open('/'.join(fotosPath,file),mode='r')

        # applies tailing to the image to extract patches from the image
        tailedImages=tailing.tailing(image=photoLocation) 

        # loops through every patch extracted to store it in the indicate pathFile and updates the database with such information
        for i in range(0, tailedImages.shape[0]):
            
            # generates the label for the patch
            labelPreprocessing.setSampleLabel(sampleLabel=file) # sets the sample label as the name of the file
            labelPreprocessing.setPreprocessingType(preprocessingType='tailing') # sets the preprocessing type as tailing
            label=labelPreprocessing.generateSampleLabel(number=i) # generates the label for the patch

            # saves the tailed image as numpy array in the indicated path to maintian the resolution of the image
            np.save(
                file='/'.join(path.getPath(),addDataType(fileName=label,dataType='npy')),
                arr=tailedImages[i]
            )

            # updates the database with the information of the preprocessed file
            # creates a Preprocessing and JuctionPre object to update the database with the information of the preprocessed files
            PreproTable=Preprocessing(clientDataset={'PreprocessingType': 'tailing', 'filePath': path.getPath(), 'label': label}, action='add')
            JuctionTable=JunctionPre(clientDataset={'SampleID': clientAnswer['SampleID'], 'PreprocessingID': PreproTable[2]}, action='add')


        # returns actual state of the databases after the preprocessing of the file. 
        # The functions Preprocessing and JunctionPre will always provide the full database of the indicated tables
        # it is to be expected that the last results bring the required information to update on the front side
        return [PreproTable, JuctionTable]

# imports more required libraries
from app.Preprocessing.DataAugmentation import Flipping, ColorDistortion
from app.Files.Label import LabelTFRecording

# defines the function augmentation that generate augmented version of available images. 
# Two kind of augmentation techniques will be considered: flipping and color distortion
def AugmentationImages(clientAnswer:dict)->list:
    
    # gets the location of the preprocessed image to be augmented
    # this information is to be taken from the preprocessedID
    PreprocessingTable=PreprocessingTable()

    # fetches the location of the preprocessed image from the database
    imagePath=PreprocessingTable.fetchInfo(statement='''SELECT FilePath, Label FROM Preprocessing WHERE PreprocessingID={}'''.format(clientAnswer['PreprocessingID']))
    
    # gets the label used for this preprocessed image
    preprocessedLabel=imagePath[0]['Label']
    
    # gets the location of the preprocessed image to be augmented
    imagePath=imagePath[0]['FilePath']

    # checks the type of data augmentation is required to be executed.
    # There are two options: Flipping and color distortion
    if clientAnswer['Method'].lower() =='flipping':

        # creates a Flipping-object for augmenting the photos
        flipping=Flipping(flipType=clientAnswer['Method'])

        # generates the augmented image to be saved
        augmentedImage=flipping.flip(image=imagePath)

        # creates an TFRecord-object to save the TFrecord in the indicated path
        saveTFRecordsFlip=TFRecorder() # correct location of the files

        # generates the label for the creation of the file name
        augmentationLabel= LabelTFRecording(preprocessingLabel=preprocessedLabel,augmentationType='flipping')
        
        # saves the TFrecord in the indicated location
        saveTFRecordsFlip.saveTFRecord(fileName=augmentationLabel.generateTensorFlowRecordLabel(),
                                       filePath=pathFormat.changePathWindowsToWsl(path=windowsAddress), # probably the address need to be changed
                                       TFRecord=augmentedImage)
        
        # adds information to the table Augmentation 
        augmentationTable=Augmentation(clientData={'Method':clientAnswer['Method'], 'FilePath':'/'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()])},
                                       )

        # adds information to JuctionAugmentation table
        juctionAugmentationTable=JunctionAugmentation(clientData={'PreprocessingID':clientAnswer['PreprocessingID'],'AugmentationID':augmentationTable[2]})

        # adds information to table TFRecording
        TFrecordingTable=TFRecording(
              clientData={'Label':augmentationLabel.generateTensorFlowRecordLabel(),
                          'FilePath':'/'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()]),
                          'AugmentationID': augmentationTable[2]
              })
        
        # returns results for updating the status of the database at fronend.
        return [augmentationTable, juctionAugmentationTable,TFrecordingTable]

    # generates augmented pictures in TRrecord format, in which the augmentation is color distortion.
    elif clientAnswer['Method'].lower()=='color distortion':

        # creates a ColorDistortion-Object for the augmentation of the photos
        # creates a ColorDistortion-object for augmenting the photos
        colorDistorion=ColorDistortion()

        # generates the augmented image to be saved
        augmentedImage=colorDistorion.distortColors(image=imagePath)

        # creates an TFRecord-object to save the TFrecord in the indicated path
        saveTFRecordsFlip=TFRecorder() # correct location of the files

        # generates the label for the creation of the file name
        augmentationLabel= LabelTFRecording(preprocessingLabel=preprocessedLabel,augmentationType='flipping')
        
        # saves the TFrecord in the indicated location
        saveTFRecordsFlip.saveTFRecord(fileName=augmentationLabel.generateTensorFlowRecordLabel(),
                                       filePath=pathFormat.changePathWindowsToWsl(path=windowsAddress), # probably the address need to be changed
                                       TFRecord=augmentedImage)
        
        # adds information to the table Augmentation 
        augmentationTable=Augmentation(clientData={'Method':clientAnswer['Method'], 'FilePath':'/'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()])},
                                       )
        
        # adds information to JuctionAgumentation table
        juctionAugmentationTable=JunctionAugmentation(clientData={'PreprocessingID':clientAnswer['PreprocessingID'],'AugmentationID':augmentationTable[2]})

        # returns results for updating the status of the database at fronend.
        return [augmentationTable, juctionAugmentationTable]

    else:

        # informs that something wrong has happened and need addressing
        print('An error has ocurred. Please review the entry "Method" and try again.')
        


