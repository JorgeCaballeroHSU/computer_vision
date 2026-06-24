# main.py

# imports required libraries for endpoint creation
from fastapi import FastAPI, File, HTTPException, UploadFile 
from pydantic import BaseModel
from typing import Optional
import os

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles



#from app.Sockets.SocketServer import SocketServer
from app.Tools.ChangePath import ChangePath
from app.dataBaseFill import dataBaseFill, PreprocessingImages, AugmentationImages
from app.trainModel import trainModel
from app.prediction import prediction

# imports libraries for the creation of the squema and the managament of the tables
from app.Database.Database import Schema
from app.Database.Tables.Tables import *


# defines the variable app that will be used to call functions. Backend application object
app=FastAPI()

# gets the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# defines the location of the database
databaseLocation=os.path.join(BASE_DIR,'database/database.db')

# calls index.html
@app.get("/")
def loadPage():
    return FileResponse(os.path.join(BASE_DIR, "templates", "index.html"))

# calls annotation.html
@app.get("/annotation")
def annotation():
    return FileResponse(os.path.join(BASE_DIR, "templates", "annotation.html"))

# calls training.html
@app.get("/training")
def annotation():
    return FileResponse(os.path.join(BASE_DIR, "templates", "training.html"))

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# calls prediction.html
@app.get("/prediction")
def annotation():
    return FileResponse(os.path.join(BASE_DIR, "templates", "prediction.html"))

app.mount("/static", StaticFiles(directory="static", html=True), name="static")




# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

# creates the database schema of the application
schemaCreation=Schema(dbFile=databaseLocation) 


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

    # checks if the client is actually sending data
    if request.clientDataset is None:
        raise HTTPException(status_code=400, detail="clientDataset is required")

    # creates an instance of the table Dataset
    table=DatasetTable(dbFile=databaseLocation)

    # opens connection to table
    table.openConnection()

    # executes the function
    results=Dataset(clientDataset=request.clientDataset, table=table,action=request.action)

    # closes connection
    table.closeConnection()

    # returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }

# gets a list of items in the table dataset
@app.get("/dataset/latest")
def getDataset():

    # creates an instance of the table Dataset
    table=DatasetTable(dbFile=databaseLocation)

    # opens conection to table
    table.openConnection()

    # fetches table Dataset
    results=table.fetchDataset()

    # closes connection to table
    table.closeConnection()

    # returns results. For now, the last result.
    return results[-1] if results else None


################## CAMERA INFO ################
# writes, updates, and deletes an item of the CameraInfo table
@app.post("/camera-info")
def handleCameraInfo(request: TableRequest):

    # checks if the client is actually sending data
    if request.clientDataset is None:
        raise HTTPException(status_code=400, detail="CameraInfo is required")
       
    # creates an instance of the table CameraInfo
    table = CameraInfoTable(dbFile=databaseLocation)

    # opens conection to table
    table.openConnection()

    # opens connection to table
    table.openConnection()

    # executes the function
    results = CameraInfo(clientDataset=request.clientDataset, table=table, action=request.action)
    
    # closes connection
    table.closeConnection()

    # returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }

# gets list of items in the CameraInfo table
@app.get("/camera-info/latest")
def getCameraInfo():

    # creates an instance of the table CameraInfo
    table = CameraInfoTable(dbFile=databaseLocation)

    # opens conection to table
    table.openConnection()

    # fetches table CameraInfo
    results=table.fetchCameraInfo()

    # closes connection to table
    table.closeConnection()

    # returns results. For now, the last result.
    return results[-1] if results else None


############## MATERIAL TYPE#########################
# writes, updates, and deletes an item of the MaterialType table
@app.post("/material-type")
def handleMaterialType(request: TableRequest):

    
    if request.clientDataset is None:
        raise HTTPException(status_code=400, detail="MaterialType is required")

    # creates an instance of the table MaterialType
    table = MaterialTypeTable(dbFile=databaseLocation)

    # opens connection to table
    table.openConnection()

    # gets the results from the table
    results = MaterialType(
        clientDataset=request.clientDataset,
        table=table,
        action=request.action
    )

    # closes connection to the table
    table.closeConnection()

    #returns results
    return {
        'success': results[0],
        'data': results[1],
        'lastID': results[2]
    }


# gets list of items in the MaterialType table
@app.get("/material-type/latest")
def handleMaterialType():

    # creates an instance of the table MaterialType
    table = MaterialTypeTable(dbFile=databaseLocation)

    # opens connection to table
    table.openConnection()

    # gets the database
    results = table.fetchMaterialType()

    # closes connection to the table
    table.closeConnection()

    # returns results
    return results[-1] if results else None


####### SAMPLE #######

# defines the input format table Sample
class SampleRequest(BaseModel):
    clientDataset: dict
    image: str

# writes, updates, and deletes an item of the Sample table
@app.post("/sample")
def handleSample(request:SampleRequest):

    # sends an error message back to front end when there is no data coming in
    if request.clientDataset is None:
        raise HTTPException(status_code=400, detail="Dataset is required")

    ############-----> I AM HERE <------#############
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