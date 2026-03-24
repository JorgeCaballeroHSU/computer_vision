#imports required libraries
from Sockets.SocketServer import SocketServer
from Tools.ChangePath import ChangePath
from Tools.Format import addDataType
from Files.Path import Path
from Files.Label import Label

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()




# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(socketServer:SocketServer, label:Label,path:Path)->str:
    
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

    # creates a file where the image is going to be saved
    with open(
        file=''.join(path.getPath(),addDataType(fileName=label.generateLabel(),dataType='jpeg')),
        mode='wb'
        ) as f:

        # saves the file
        f.write(clientAnswer) #-> client answer contains the image as binary

        # closes the file when is over
        f.close()

    # asks client about the metadata the latest file
    socketServer.send('send metadata')

    # gets metadata from the image
    clientAnswer=socketServer.receive().decode() #---> files comes as a dictionary

    # transforms the image

    # makes the TFrecord


    return None