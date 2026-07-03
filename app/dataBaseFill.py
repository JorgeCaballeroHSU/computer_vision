#imports required libraries
from app.Tools.ChangePath import ChangePath
from app.Tools.Format import addDataType
from app.Files.Path import Path
from app.Files.Label import LabelPreprocessing, LabelSample
from app.Database.Tables.Tables import *
from app.Preprocessing.TFRecorder import TFRecorder
import os
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
                "path": filePath,
                "SampleID":lastId
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

# imports required libraries
from app.Preprocessing.Tailing import Tailing

# Preprocesses the images by applying tailing
def PreprocessingImages(clientAnswer: dict, dbFile: str):

    """
    Applies tailing preprocessing to all images in background
    """

    def worker():

        db=None

        try:
            tailing = Tailing(size=512, stride=206)
            pathManager = Path(dbFile=dbFile)

            fotosPath = pathManager.loadPath("tfrecord")

            #✅ Initialize TFRecorder
            tfRecorder = TFRecorder(tfrecordDir=fotosPath)
           
            # opens connection to the database
            db = Database(dbFile)
            db.openConnection()

            
            rawRecords = db.fetchInfo(
                """
                SELECT Label,
                FilePath,
                TFRecordingID
            FROM TFRecording
                """
            )

            for recordInfo in rawRecords:

                fullPath = recordInfo["FilePath"]

                dataset = tfRecorder.readTFRecord(fullPath)
                
                for image, label, labelInit in dataset:
                    
                    
                    print(
                        f"Preprocessing {recordInfo['Label']} "
                        f"shape={image.shape}"
                    )

                    if image.shape[0] < 512 or image.shape[1] < 512:
                        print(
                            f"⚠️ Skipping image because shape is {image.shape}"
                        )
                        continue

                    tailedImages = tailing.tailing(image=image)

                    for i in range(tailedImages.shape[0]):

                        labelGen = LabelPreprocessing(
                            sampleLabel=recordInfo["Label"],
                            preprocessingType='tailing'
                        )

                        labelOut = labelGen.generatePreprocessingLabel(number=i)

                        tfFileName = addDataType(labelOut, "tfrec")

                        record = tfRecorder.createTFRecordFromTensor(
                            image=tailedImages[i],
                            label=labelOut,
                            labelInit=1
                        )

                        tfRecorder.saveTFRecord(
                            fileName=tfFileName,
                            filePath=fotosPath,
                            TFRecord=record
                        )

                        tfPath = os.path.join(fotosPath, tfFileName)
                        
                        # Insert preprocessing record
                        preprocessingID, _ = db.insertItemsTable(
                            query="""
                                INSERT INTO Preprocessing
                                (PreprocessingType, FilePath, Label)
                                VALUES (?, ?, ?)
                            """,
                            values=(
                                'tailing',
                                tfPath,
                                labelOut
                            )
                        )

                        # Obtain TFRecordingID from the source TFRecord label
                        sourceLabel = label.numpy().decode("utf-8")

                        tfRecord = db.fetchInfo(
                            """
                            SELECT TFRecordingID
                            FROM TFRecording
                            WHERE Label = ?
                            """,
                            (sourceLabel,)
                        )

                        if not tfRecord:
                            print(f"❌ TFRecording not found for {sourceLabel}")
                            continue

                        tfRecordID = tfRecord[0]["TFRecordingID"]

                        # Create junction
                        db.insertItemsTable(
                            query="""
                                INSERT INTO JunctionPre
                                (TFRecordingID, PreprocessingID)
                                VALUES (?, ?)
                            """,
                            values=(
                                tfRecordID,
                                preprocessingID
                            )
                        )

                        # ----------------------------------------
                        # Automatic augmentations
                        # ----------------------------------------

                        # Horizontal flip
                        AugmentationImages(
                            clientAnswer={
                                "PreprocessingID": preprocessingID,
                                "Method": "flippinghorizontal"
                            },
                            dbFile=dbFile
                        )

                        # Vertical flip
                        AugmentationImages(
                            clientAnswer={
                                "PreprocessingID": preprocessingID,
                                "Method": "flippingvertical"
                            },
                            dbFile=dbFile
                        )

                        # Color distortion
                        AugmentationImages(
                            clientAnswer={
                                "PreprocessingID": preprocessingID,
                                "Method": "color distortion"
                            },
                            dbFile=dbFile
                        )
            
            

            # indicates that the preprocessing is complete
            print("✅ Preprocessing complete")

        except Exception as e:
            print(f"[Preprocessing ERROR] {e}")

        finally:
            
            if db:
                # closes the connection to the database
                db.closeConnection()

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

        db=None
        
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

            tfPath = result[0]['FilePath']
            preLabel = result[0]['Label']

            tfRecorder = TFRecorder(tfrecordDir=os.path.dirname(tfPath))

            dataset = tfRecorder.readTFRecord(tfPath)

            method = clientAnswer['Method'].lower()

            # ✅ Prevent duplicates
            existing = db.fetchInfo(
                """
                SELECT *
                FROM Augmentation
                WHERE Method = ?
                AND FilePath LIKE ?
                """,
                (
                    clientAnswer['Method'],
                    f"%{preLabel}%"
                )
            )

            if existing:
                print("✅ Already augmented")
                return
 
            
            dataset = tfRecorder.readTFRecord(tfPath)

            try:
                image, label, labelInit = next(iter(dataset))
            except StopIteration:
                print(f"❌ Empty TFRecord: {tfPath}")
                return

            print(
                f"Loaded augmentation image: "
                f"{preLabel} "
                f"shape={image.shape}"
            )

            # ✅ Apply augmentation
            if method == "flippinghorizontal":

                augmenter = Flipping(
                    flipType="horizontal"
                )

                augmented = augmenter.flip(image=image)
                augType = "flippinghorizontal"

            elif method == "flippingvertical":

                augmenter = Flipping(
                    flipType="vertical"
                )

                augmented = augmenter.flip(image=image)
                augType = "flippingvertical"

            elif method == "color distortion":

                augmenter = ColorDistortion()

                augmented = augmenter.distortColors(
                    image=image
                )

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

            basePath = Path(dbFile).loadPath("tfrecord")
            tfFile = addDataType(tfLabel, "tfrec")
            tfPath = os.path.join(basePath, tfFile)

            # ✅ Save TFRecord
            record = tfRecorder.createTFRecordFromTensor(
                image=augmented,
                label=tfLabel,
                labelInit=int(labelInit.numpy())
            )

            tfRecorder.saveTFRecord(
                fileName=tfFile,
                filePath=basePath,
                TFRecord=record
            )

            # ✅ Insert Augmentation
            augID, _ = db.insertItemsTable(
                query="""
                    INSERT INTO Augmentation
                    (Method, FilePath)
                    VALUES (?, ?)
                """,
                values=(
                    clientAnswer['Method'],
                    tfPath
                )
            )

            # ✅ Junction table
            db.insertItemsTable(
                query="""
                    INSERT INTO JunctionAugmentation
                    (PreprocessingID, AugmentationID)
                    VALUES (?, ?)
                """,
                values=(
                    clientAnswer['PreprocessingID'],
                    augID
                )
            )    

            print(f"✅ Augmentation completed: {tfLabel}")

        except Exception as e:
            print(f"[Augmentation ERROR] {e}")

        finally:
            if db:
                db.closeConnection()

    Thread(target=worker, daemon=True).start()
        


