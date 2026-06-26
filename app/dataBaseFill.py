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
    Background worker that ensures every Sample has a TFRecord.
    """

    def worker():
        try:
            database.openConnection()

            samples = database.fetchInfo("SELECT Label, FilePath FROM Sample")

            for sample in samples:

                label = sample["Label"]
                imagePath = sample["FilePath"]

                existing = database.fetchInfo(
                    "SELECT * FROM TFRecording WHERE Label = ?",
                    (label,)
                )

                if existing:
                    continue

                try:
                    record = tfRecorder.createTFRecord(
                        fileName=imagePath,
                        label=label,
                        labelInit=1
                    )

                    tfFileName = addDataType(label, "tfrec")
                    tfPath = os.path.join(path.getPath(), tfFileName)

                    tfRecorder.saveTFRecord(
                        fileName=tfFileName,
                        filePath=path.getPath(),
                        TFRecord=record
                    )

                    database.insertItemsTable(
                        query="INSERT INTO TFRecording (Label, FilePath, AugmentationID) VALUES (?, ?, NULL)",
                        values=(label, tfPath)
                    )

                except Exception as e:
                    print(f"[TFRecord ERROR] {label}: {e}")

            database.closeConnection()

        except Exception as e:
            print(f"[TF Background ERROR] {e}")

    Thread(target=worker, daemon=True).start()


# imports required libraries
from app.Preprocessing import Tailing

# Preprocesses the images by applying tailing
def PreprocessingImages(clientAnswer: dict, dbFile: str):

    """
    Applies tailing preprocessing to all images in background
    """

    def worker():
        try:
            tailing = Tailing(size=512, stride=512)
            pathManager = Path(dbFile=dbFile)

            fotosPath = pathManager.loadPath("image")

            filesAvailable = os.listdir(fotosPath)

            for file in filesAvailable:

                fullPath = os.path.join(fotosPath, file)

                # ✅ FIX: open image correctly
                photoLocation = fullPath

                tailedImages = tailing.tailing(image=photoLocation)

                for i in range(tailedImages.shape[0]):

                    labelGen = LabelPreprocessing(
                        sampleLabel=file,
                        preprocessingType='tailing'
                    )

                    label = labelGen.generateSampleLabel(number=i)

                    npyPath = os.path.join(
                        fotosPath,
                        addDataType(label, 'npy')
                    )

                    np.save(file=npyPath, arr=tailedImages[i])

                    # ✅ Insert into DB
                    preTable = Preprocessing(
                        clientDataset={
                            'PreprocessingType': 'tailing',
                            'FilePath': npyPath,
                            'Label': label
                        },
                        table=PreprocessingTable(dbFile),
                        action='add'
                    )

                    JunctionPre(
                        clientDataset={
                            'SampleID': clientAnswer['SampleID'],
                            'PreprocessingID': preTable[2]
                        },
                        table=JunctionPreTable(dbFile),
                        action='add'
                    )

            print("✅ Preprocessing complete")

        except Exception as e:
            print(f"[Preprocessing ERROR] {e}")

    Thread(target=worker, daemon=True).start()

# imports more required libraries
from app.Preprocessing.DataAugmentation import Flipping, ColorDistortion
from app.Files.Label import LabelTFRecording

# defines the function augmentation that generate augmented version of available images. 
# Two kind of augmentation techniques will be considered: flipping and color distortion
def AugmentationImages(clientAnswer: dict, dbFile: str):

    """
    Background augmentation pipeline
    """

    def worker():
        try:
            db = Database(dbFile)
            db.openConnection()

            # ✅ Fetch preprocessing info safely
            result = db.fetchInfo(
                "SELECT FilePath, Label FROM Preprocessing WHERE PreprocessingID = ?",
                (clientAnswer['PreprocessingID'],)
            )

            if not result:
                print("❌ Preprocessing not found")
                return

            imagePath = result[0]['FilePath']
            preLabel = result[0]['Label']

            method = clientAnswer['Method'].lower()

            # ✅ Prevent duplicates
            existing = db.fetchInfo(
                "SELECT * FROM Augmentation WHERE Method = ? AND FilePath LIKE ?",
                (clientAnswer['Method'], f"%{preLabel}%")
            )

            if existing:
                print("✅ Already augmented")
                return

            # ✅ Apply augmentation
            if method == "flipping":
                augmenter = Flipping(flipType=clientAnswer['Method'])
                augmented = augmenter.flip(image=imagePath)
                augType = "flipping"

            elif method == "color distortion":
                augmenter = ColorDistortion()
                augmented = augmenter.distortColors(image=imagePath)
                augType = "color"

            else:
                print("❌ Invalid method")
                return

            # ✅ Generate label
            labelGen = LabelTFRecording(
                preprocessingLabel=preLabel,
                augmentationType=augType
            )

            tfLabel = labelGen.generateTensorFlowRecordLabel()

            basePath = Path(dbFile).loadPath("image")
            tfFile = addDataType(tfLabel, "tfrec")
            tfPath = os.path.join(basePath, tfFile)

            # ✅ Save TFRecord
            tfRecorder = TFRecorder()
            tfRecorder.saveTFRecord(
                fileName=tfFile,
                filePath=basePath,
                TFRecord=augmented
            )

            # ✅ Insert Augmentation
            augResult = Augmentation(
                clientData={
                    'Method': clientAnswer['Method'],
                    'FilePath': tfPath
                },
                table=AugmentationTable(dbFile),
                action='add'
            )

            augID = augResult[2]

            # ✅ Junction table
            JunctionAugmentation(
                clientData={
                    'PreprocessingID': clientAnswer['PreprocessingID'],
                    'AugmentationID': augID
                },
                table=JunctionAugmentationTable(dbFile),
                action='add'
            )

            # ✅ TFRecording table
            TFRecording(
                clientData={
                    'Label': tfLabel,
                    'FilePath': tfPath,
                    'AugmentationID': augID
                },
                table=TFRecordingTable(dbFile),
                action='add'
            )

            db.closeConnection()

            print(f"✅ Augmentation completed: {tfLabel}")

        except Exception as e:
            print(f"[Augmentation ERROR] {e}")

    Thread(target=worker, daemon=True).start()
        


