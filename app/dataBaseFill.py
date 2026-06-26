#imports required libraries
from app.Tools.ChangePath import ChangePath
from app.Tools.Format import addDataType
from app.Files.Path import Path
from app.Files.Label import LabelPreprocessing, LabelSample
from app.Database.Tables.Tables import *
from app.Preprocessing.TFRecorder import TFRecorder
import os
import numpy as np
from threading import Thread


# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

def dataBaseFill(clientAnswer: dict, action: str, file, dbFile: str) -> dict:
    """
    Safe pipeline:
    DB first → file second → rollback if needed
    """

    try:
        label = LabelSample(dbFile=dbFile)
        pathManager = Path(dbFile=dbFile)

        if action != "add":
            return {"success": False}

        if file is None:
            return {"success": False, "message": "File missing"}

        # ✅ Generate label
        labelFile = label.generateSampleLabel()
        if not labelFile:
            return {"success": False, "message": "Label generation failed"}

        basePath = pathManager.loadPath("image")
        filePath = os.path.join(basePath, addDataType(labelFile, "jpg"))

        # ✅ Get IDs
        db = Database(dbFile=dbFile)
        cameraInfoID = db.fetchLastID("CameraInfo", "CameraInfoID")
        datasetID = db.fetchLastID("Dataset", "datasetID")
        materialTypeID = db.fetchLastID("MaterialType", "MaterialTypeID")

        # ✅ Prepare DB payload
        clientDataset = {
            'Label': labelFile,
            'FilePath': filePath,  # ✅ FULL path (not basePath!)
            'CaptureTime': clientAnswer.get('CaptureTime'),
            'CameraInfoID': cameraInfoID,
            'DatasetID': datasetID,
            'MaterialTypeID': materialTypeID
        }

        table = SampleTable(dbFile=dbFile)

        try:
            # ✅ OPEN connection
            table.openConnection()

            # ✅ TRY INSERT FIRST
            lastId = table.insertSampleTable(clientAnswer=clientDataset)

            if lastId == -1:
                raise Exception("Database insert failed")

            # ✅ ONLY NOW WRITE FILE
            with open(filePath, "wb") as buffer:
                while True:
                    chunk = file.file.read(1024 * 1024)  # 1MB
                    if not chunk:
                        break
                    buffer.write(chunk)

            # ✅ COMMIT ALREADY DONE INSIDE insert
            return {
                "success": True,
                "label": labelFile,
                "path": filePath
            }

        except Exception as e:
            print(f"[dataBaseFill] ERROR: {e}")

            # ✅ ROLLBACK DB if file fails
            try:
                table.deleteSampleTable({'SampleID': lastId})
            except:
                pass

            return {
                "success": False,
                "message": str(e)
            }

        finally:
            table.closeConnection()

    except Exception as e:
        print(f"[dataBaseFill] Fatal Error: {e}")
        return {"success": False, "message": str(e)}

        

def generateTensorFlowRecordsBackground(path: Path, database: Database, tfRecorder: TFRecorder):
    """
    Background worker that scans all samples and ensures each one has a TFRecord.

    Behavior:
    - Iterates over all samples in the database
    - Checks if a TFRecord already exists
    - If not → creates TFRecord
    - Safe to run multiple times (idempotent)

    This function is designed to run in the background.
    """

    def worker():
        try:
            database.openConnection()

            # ----------------------------------------
            # ✅ 1. Get all samples
            # ----------------------------------------
            samples = database.fetchInfo("SELECT Label, FilePath FROM Sample")

            for sample in samples:

                label = sample["Label"]
                imagePath = sample["FilePath"]

                # ----------------------------------------
                # ✅ 2. Check if TFRecord exists
                # ----------------------------------------
                existing = database.fetchInfo(
                    "SELECT * FROM TFRecording WHERE Label = ?",
                    (label,)
                )

                if existing:
                    print(f"✅ TFRecord already exists for {label}")
                    continue  # skip

                print(f"⚙️ Creating TFRecord for {label}")

                # ----------------------------------------
                # ✅ 3. Create TFRecord
                # ----------------------------------------
                try:
                    record = tfRecorder.createTFRecord(
                        fileName=imagePath,
                        label=label,
                        labelInit=1  # your label logic here (or map)
                    )

                    tfRecordName = f"{label}.tfrec"
                    tfRecordPath = os.path.join(path.getPath(), tfRecordName)

                    # save to disk
                    tfRecorder.saveTFRecord(
                        fileName=tfRecordName,
                        filePath=path.getPath(),
                        TFRecord=record
                    )

                    # ----------------------------------------
                    # ✅ 4. Insert into DB (mark as processed)
                    # ----------------------------------------
                    database.insertItemsTable(
                        query='''
                            INSERT INTO TFRecording (Label, FilePath)
                            VALUES (?, ?)
                        ''',
                        values=(label, tfRecordPath)
                    )

                    print(f"✅ TFRecord created for {label}")

                except Exception as e:
                    print(f"❌ Failed for {label}: {e}")

            database.closeConnection()

        except Exception as e:
            print(f"[Background TFRecord] Error: {e}")

    # ----------------------------------------
    # ✅ Run in background thread
    # ----------------------------------------
    thread = Thread(target=worker, daemon=True)
    thread.start()



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
        photoLocation= open('\\'.join(fotosPath,file),mode='r')

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
                file='\\'.join(path.getPath(),addDataType(fileName=label,dataType='npy')),
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
        augmentationTable=Augmentation(clientData={'Method':clientAnswer['Method'], 'FilePath':'\\'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()])},
                                       )

        # adds information to JuctionAugmentation table
        juctionAugmentationTable=JunctionAugmentation(clientData={'PreprocessingID':clientAnswer['PreprocessingID'],'AugmentationID':augmentationTable[2]})

        # adds information to table TFRecording
        TFrecordingTable=TFRecording(
              clientData={'Label':augmentationLabel.generateTensorFlowRecordLabel(),
                          'FilePath':'\\'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()]),
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
        augmentationTable=Augmentation(clientData={'Method':clientAnswer['Method'], 'FilePath':'\\'.join([pathFormat.changePathWindowsToWsl(path=windowsAddress),augmentationLabel.generateTensorFlowRecordLabel()])},
                                       )
        
        # adds information to JuctionAgumentation table
        juctionAugmentationTable=JunctionAugmentation(clientData={'PreprocessingID':clientAnswer['PreprocessingID'],'AugmentationID':augmentationTable[2]})

        # returns results for updating the status of the database at fronend.
        return [augmentationTable, juctionAugmentationTable]

    else:

        # informs that something wrong has happened and need addressing
        print('An error has ocurred. Please review the entry "Method" and try again.')
        


