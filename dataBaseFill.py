#imports required libraries
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



    # updates the database's table with the metadata and image location
    # updates table label
    database.insertItemsTable( # this has to check if the label type already exists in the database, if it already exists, there is no need to add a thing.
        query='''INSERT INTO label (name, labelType) VALUES (?, ?) ''',
        values=(labelFile,                      # labelfile is the label of the picture.
                clientAnswer.pop('labelType'))      # LabelType corresponds to the type of label. S, K, T or M
    )

    # updates the cameraInfo table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    database.insertItemsTable(# correct<<<-------
        query='''INSERT INTO cameraInfo (Manufacturer, CameraModel, ISO, Focus, Exposuretime, FlashMode, FocalLength, Objective, Extension) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
        values=(clientAnswer.pop('Manufacturer'),       # Manufacturer corresponds to the manufacturer of the camera used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('CameraModel'),        # CameraModel corresponds to the model of the camera used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('ISO'),                # ISO corresponds to the ISO used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('Focus'),              # Focus corresponds to the focus used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('Exposuretime'),       # Exposuretime corresponds to the exposure time used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('FlashMode'),          # FlashMode corresponds to the flash mode used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('FocalLength'),        # FocalLength corresponds to the focal length used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('Objective'),          # Objective corresponds to the objective used to take the picture. It is obtained from the exif data of the picture.
                clientAnswer.pop('Extension'))          # Extension corresponds to the extension used to take the picture. It is obtained from the exif data of the picture.
    )

    # updates the Dataset table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    database.insertItemsTable(
        query='''INSERT INTO Dataset (name, ProjectName, Created, Description) VALUES (?, ?, ?, ?) ''',
        values=(labelFile, clientAnswer.pop('ProjectName'), clientAnswer.pop('Created'), clientAnswer.pop('Description'))
    )

    # updates the MaterialType table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    database.insertItemsTable(
        query='''INSERT INTO MaterialType (mm0063, mm0125, mm0250, mm0400, mm0500, mm1000, mm2000, mm4000, mm8000, mm1600, mm3200) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
        values=(
            clientAnswer.pop('mm0063'),                 # mm0063 corresponds to the value of the material type for the size of 0.063 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm0125'),                 # mm0125 corresponds to the value of the material type for the size of 0.125 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm0250'),                 # mm0250 corresponds to the value of the material type for the size of 0.250 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm0400'),                 # mm0400 corresponds to the value of the material type for the size of 0.400 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm0500'),                 # mm0500 corresponds to the value of the material type for the size of 0.500 mm. It is obtained from the exif data of the picture.  
            clientAnswer.pop('mm1000'),                 # mm1000 corresponds to the value of the material type for the size of 1.000 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm2000'),                 # mm2000 corresponds to the value of the material type for the size of 2.000 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm4000'),                 # mm4000 corresponds to the value of the material type for the size of 4.000 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm8000'),                 # mm8000 corresponds to the value of the material type for the size of 8.000 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm1600'),                 # mm1600 corresponds to the value of the material type for the size of 16.000 mm. It is obtained from the exif data of the picture.
            clientAnswer.pop('mm3200'))                 # mm3200 corresponds to the value of the material type for the size of 32.000 mm. It is obtained from the exif data of the picture.
    )

    # updates table sample 
    database.insertItemsTable(
        query='''INSERT INTO Sample (filePath, captureTime, isProcessed, path) VALUES (?, ?, ?, ?) ''',
        values=(label._sampleNumber, clientAnswer.pop('name'), clientAnswer.pop('labelType'), ''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')))
    )

    # returns the answer of the client with the rest of information to be added to the database
    return clientAnswer    

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


# makes the TFrecord