# main.py

# imports required libraries for endpoint creation
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from typing import Optional


from Sockets.SocketServer import SocketServer
from Tools.ChangePath import ChangePath
from dataBaseFill import dataBaseFill, PreprocessingImages, AugmentationImages
from trainModel import trainModel
from prediction import prediction

# imports libraries for the creation of the squema and the managament of the tables
from Database.Database import Schema
from Database.Tables.Tables import *


# defines the variable app that will be used to call functions. Backend application object
app=FastAPI()

# defines the location of the database
databaseLocation=r'/home/helmut-schmidt-universitaet/Documents/Computer Vision Project/Database/database.db' #---> to be corrected

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

# creates the database schema of the application
schemaCreation=Schema(dbFile=databaseLocation) 
schemaCreation.closeConnection() # ---> Closes the connection

####### GETS THE PCITURES FROM CLIENT #######
# gets the pictures from the frontend and saves them in a folder
@app.post("/upload-image")
def handleImage(file: UploadFile = File(...)):

    # opens try block to catch errors
    try:

        # opens the file and saves it in the indicated location
        with open(pathFormat.changePathWindowsToWsl(path=windowsAddress)+"/"+file.filename, "wb") as buffer:
            while contents := file.file.read(1024 * 1024):
                buffer.write(contents)

    # catches exceptions and raises an HTTPException with status code 500 and a detail message
    except Exception:
        raise HTTPException(status_code=500, detail="Error uploading the file")
    
    finally:
        file.file.close()

    # restuns a success message if the file is uploaded successfully
    return {"message": "File uploaded successfully"}


#### DATASET TABLE########
# defines the input format for most of the tables
class TableRequest(BaseModel):
    clientDataset: Optional[dict]
    action: str='add'


# writes, updates, and deletes a item of the Dataset table
@app.post("/dataset")
def handleDataset(request:TableRequest):

    # creates an instance of the table Dataset
    table=DatasetTable()

    # executes the function
    results=Dataset(clientDataset=request.clientDataset, table=table,action=request.action)

    # returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }

# gets a list of items in the table dataset
@app.get("/dataset")
def handleDataset():

    # creates an instance of the table Dataset
    table=DatasetTable()

    # returns results
    return table.fetchDataset()


################## CAMERA INFO ################
# writes, updates, and deletes an item of the CameraInfo table
@app.post("/camera-info")
def handleCameraInfo(request: TableRequest):

    # creates an instance of the table CameraInfo
    table = CameraInfoTable("your_database.db")

    # executes the function
    results = CameraInfo(
        clientDataset=request.clientDataset,
        table=table,
        action=request.action
    )

    # returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }

# gets list of items in the CameraInfo table
@app.get("/camera-info")
def handleCameraInfo():

    # creates an instance of the table CameraInfo
    table = CameraInfoTable("your_database.db")

    # returns results
    return table.fetchCameraInfo()


############## MATERIAL TYPE#########################
# writes, updates, and deletes an item of the MaterialType table
@app.post("/material-type")
def handleMaterialType(request: TableRequest):

    # creates an instance of the table MaterialType
    table = MaterialTypeTable("your_database.db")

    # executes the function
    results = MaterialType(
        clientDataset=request.clientDataset,
        table=table,
        action=request.action
    )

    # returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }


# gets list of items in the MaterialType table
@app.get("/material-type")
def handleMaterialType():

    # creates an instance of the table MaterialType
    table = MaterialTypeTable("your_database.db")

    # returns results
    return table.fetchMaterialType()

####### SAMPLE #######

# defines the input format table Sample
class SampleRequest(BaseModel):
    clientDataset: dict
    image: str

# writes, updates, and deletes an item of the Sample table
@app.post("/sample")
def handleSample(request:SampleRequest):

    # gets the results from the function dataBaseFill
    results=dataBaseFill(clientDataset=request.clientDataset,image=request.image)

    # returns results
    return results

####### PREPROCESSING ########
# defines the input format table preprocessing and junctionPre
class PreprocessingRequest(BaseModel):
    PreprocessingType: str
    filePath: str
    label: str
    SampleID: int

# writes, updates, and deletes an item of the Preprocessing table and the JunctionPre table
@app.post("/preprocessing")
def handlePreprocessing(request:PreprocessingRequest):

    # gets the result form the function PreprocessingImages
    results=PreprocessingImages(clientDataset={
        'PreprocessingType': request.PreprocessingType, 
        'filePath': request.filePath, 
        'label': request.label, 
        'SampleID': request.SampleID}, 
                          action='add')
    
    # returns results
    return results

###### AUGMENTATION ########
# defines the input format for table Augmentation and JuctionAugmentation
class AugmentationRequest(BaseModel):
    Method:str
    FilePath:str
    PreprocessingID: int

# writes, updates, and deletes an item of the Augmentation and JunctionAugmentation tables
@app.post("/augmentation")
def handleAugmentation(request:AugmentationRequest):

    # gests the restults from the function AugmentationImages
    results=AugmentationImages(clientDataset={
        'Method':request.Method,
        'FilePath':request.FilePath,
        'PreprocessingID':request.PreprocessingID
    })

    # return results
    return results