#imports required libraries
from Sockets.SocketServer import SocketServer
from Tools.ChangePath import ChangePath
from Tools.Format import addDataType
from Files.Path import Path
from Files.Label import Label
from Database.Database import Database
from Preprocessing.TFRecorder import TFRecorder
import os

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(socketServer:SocketServer, label:Label,path:Path, database:Database)->str:
    
    # asks the client to send the image 
    socketServer.send(
        toSend='send photos'
    )

    # loops check if the client is ready to send images
    while True:
        
        # gets the answer of the client. It indicates whether it is ready to send the images
        clientAnswer=socketServer.receive().decode()

        # if the answer of the client is True, then start downloading the images
        if clientAnswer==True:
            
            # receives image from client
            clientAnswer=socketServer.receive().decode()

            # breaks the loop and continues with the next process
            break

        elif clientAnswer==False:

            #stays in the loop
            continue
    

    # stores original image in predefined location
    # sets the path to save the files
    path.setPath(path=pathFormat.changePathWindowsToWsl(path=windowsAddress))

    # saves the path in the database
    path.savePath()

    # generates label
    labelFile=label.generateLabel()

    # creates a file where the image is going to be saved
    with open(
        file=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')),
        mode='wb'
        ) as f:

        # saves the file
        f.write(clientAnswer) #-> client answer contains the image as binary

        # closes the file when is over
        f.close()

    # asks client about the metadata the latest file
    socketServer.send('send metadata')

    # gets metadata from the image
    imageMetadata:dict=socketServer.receive().decode() #---> files comes as a dictionary

    # adds information to database
    # adds metadata & image
    database.addItemImagMeta(
        label= labelFile,
        date= imageMetadata.date,
        length=imageMetadata.length,
        width=imageMetadata.width,
        size=imageMetadata.size,
        manuf=imageMetadata.manuf,
        cameraMode=imageMetadata.cameraMode,
        ISO=imageMetadata.ISO,
        focus=imageMetadata.focus,
        exposureTime=imageMetadata.exposureTime,
        flashMode=imageMetadata.flashMode,
        focalLength=imageMetadata.focalLength,
        objective=imageMetadata.objective,
        extension=imageMetadata.extension,
        preprocessed=imageMetadata.preprocessed,
        author=imageMetadata.author,
        copyright=imageMetadata.copyright,
        location=imageMetadata.location,
        IDTF=1, ###-----> to be corrected
    )

    return None    

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