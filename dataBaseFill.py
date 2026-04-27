#imports required libraries
from importlib.resources import path

from Sockets.SocketServer import SocketServer
from Tools.ChangePath import ChangePath
from Tools.Format import addDataType
from Files.Path import Path
from Files.Label import Label
from Database.Database import Database
from Preprocessing.TFRecorder import TFRecorder
import os
from PIL import Image
from PIL.ExifTags import TAGS

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(socketServer:SocketServer, label:Label,path:Path, database:Database)->dict:
    
    # gets the image from the client
    # It assumes that the client will send the image as chucks that will be put together at the socket class
    # it assumes that the picture will be received as binary that will be decoded at the socket class
    # it assumes that the pciture will be received as a part of a dictionary with some other metadata.
    # this medatadata will be used to fill up the database
    clientAnswer:dict=socketServer.receive() # it assumes that the chucks of the image will be 
    # addended together in the socker class and that the chunks of the image will be added together

    # stores the image in the defined path
    # sets the path to save the files
    path.setPath(path=pathFormat.changePathWindowsToWsl(path=windowsAddress))

    # generates label for the picture
    label.setLabelType(labelType=clientAnswer.pop('labelType')) # sets the label type
    labelFile=label.generateSampleLabel()

    # creates a file where the image is going to be saved
    with open(
        file=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')),
        mode='wb'
        ) as f:

        # saves the file
        f.write(clientAnswer.pop('image')) #-> client answer contains the image as binary

        # closes the file when is over
        f.close()


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





# imports more required libraries
from Preprocessing.DataAugmentation import Flipping, ColorDistortion

# transforms the images
def transformImages(path:Path,flip:Flipping, colDis:ColorDistortion,datenBank:Database,timesPerFoto:int=10)->None:

    # gets the path where the images are located
    fotosPath=path.getPath()

    # gets a list of files avialables in the path
    filesAvailable=os.listdir(path=fotosPath)

    #loops through every file available
    for file in filesAvailable:
        
        # generates the address of the file and opens it for use read only.
        photoLocation= open('/'.join(fotosPath,file),mode='r')

        # in this loop the transformations will be done
        for i in range(0, timesPerFoto):

            # flips the image two times randomly
            if i==0 or i==1:
                
                # flips randomly the image
                file=flip.flip(image=photoLocation)

            # distors randomly the image several times.
            # provides timesPerFoto-2 of these random distorsions
            else:

                # distors the image
                file=colDis.distortColors(image=photoLocation)

        # closes the file
        photoLocation.close()

        datenBank.addItemTFRecording(label='', TFRecoding=file)
        

    # returns None
    return None
