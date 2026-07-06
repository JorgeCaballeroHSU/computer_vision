# import required libraries
import keras
from datetime import datetime

from  app.Database.Tables.Tables import *
from app.CNN.Models import ModelFactory
import random


from app.Preprocessing.TFRecorder import TFRecorder
import tensorflow as tf
import os


def buildTrainingDataset(
        records: list,
        batchSize: int,
        shuffle: bool = True
    ) -> tf.data.Dataset:

    """
    Converts sampled TFRecords into a TensorFlow dataset.
    """

    filePaths = [
        record["FilePath"]
        for record in records
    ]

    if not filePaths:
        raise ValueError("No TFRecords available")

    tfRecorder = TFRecorder(
        tfrecordDir=os.path.dirname(filePaths[0])
    )

    dataset = tfRecorder.readMultipleTFRecords(
        fileNames=filePaths
    )

    # Keep only image and class label
    dataset = dataset.map(
        lambda image, label, labelInit:
        (image, labelInit)
    )

    if shuffle:
        dataset = dataset.shuffle(
            buffer_size=len(filePaths)
        )

    dataset = dataset.batch(batchSize)

    dataset = dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return dataset

def datasetSampling(clientAnswer: dict, dbFile: str) -> list[list, list]:
    """
    Splits dataset by preprocessing tile.

    Example:

    Training:
        tailing_00
        tailing_00_flippinghorizontal
        tailing_00_flippingvertical
        tailing_00_color

    Validation:
        tailing_01
        tailing_01_flippinghorizontal
        tailing_01_flippingvertical
        tailing_01_color

    This prevents augmentation leakage.
    """
    # Connects and opens the database connection
    db = Database(dbFile)
    db.openConnection()

    try:

        # gets the dataset ID from the client answer
        datasetID = clientAnswer["DatasetID"]

        # All preprocessing tiles
        preprocessingRecords = db.fetchInfo(
            """
            SELECT DISTINCT
                P.PreprocessingID,
                P.Label,
                P.FilePath

            FROM Sample S

            INNER JOIN JunctionPre JP
                ON JP.TFRecordingID = S.TFRecordingID

            INNER JOIN Preprocessing P
                ON P.PreprocessingID = JP.PreprocessingID

            WHERE S.DatasetID = ?
            """,
            (
                datasetID,
            )
        )

        if not preprocessingRecords:
            raise ValueError(
                f"No preprocessing records found for DatasetID={datasetID}"
            )


        groups = []

        for pre in preprocessingRecords:

            group = []

            # Base tile
            group.append({
                "Label": pre["Label"],
                "FilePath": pre["FilePath"]
            })

            # Associated augmentations
            augmentations = db.fetchInfo(
                """
                SELECT
                    Augmentation.Method,
                    Augmentation.FilePath
                FROM Augmentation
                INNER JOIN JunctionAugmentation
                    ON JunctionAugmentation.AugmentationID =
                       Augmentation.AugmentationID
                WHERE JunctionAugmentation.PreprocessingID = ?
                """,
                (pre["PreprocessingID"],)
            )

            for aug in augmentations:

                group.append({
                    "Method": aug["Method"],
                    "FilePath": aug["FilePath"]
                })

            groups.append({
                "PreprocessingID": pre["PreprocessingID"],
                "Label": pre["Label"],
                "Records": group
            })

        # Shuffle tile groups
        random.shuffle(groups)

        trainPercentage = clientAnswer["TrainingPercentage"]
        validationPercentage = clientAnswer["ValidationPercentage"]

        if trainPercentage + validationPercentage != 100:
            raise ValueError(
                "TrainingPercentage + ValidationPercentage must equal 100"
            )

        trainCount = int(
            len(groups) * trainPercentage / 100
        )

        trainingGroups = groups[:trainCount]
        validationGroups = groups[trainCount:]
        
        trainingSamples = [
            item
            for group in trainingGroups
            for item in group["Records"]
        ]
        
        validationSamples = [
            item
            for group in validationGroups
            for item in group["Records"]
        ]


        return {
            "trainingTiles": trainingGroups,
            "validationTiles": validationGroups,
            "trainingRecords": trainingSamples,
            "validationRecords": validationSamples
            }

    finally:
        db.closeConnection()



# trains the one architecture or version according the requirements of the user.
# by architecture is meant to be the type of model, for example ResNet, VGG, etc. and by version is meant an specific set of hyperparameters or combination
# of training-, testing-, and validation datasets.
# Trains only one architecture or version of an architecture at a time.
def trainModel(
        clientAnswer: dict,
        dbFile: str
    ) -> dict | None:

    db = Database(dbFile)

    db.openConnection()

    try:

        # --------------------------------------------------
        # Check if model exists
        # --------------------------------------------------

        existingModel = db.fetchInfo(
            """
            SELECT ModelID
            FROM Model
            WHERE ModelName = ?
            """,
            (
                clientAnswer["ModelName"],
            )
        )

        if existingModel:

            modelID = existingModel[0]["ModelID"]

        else:

            print(
                "The model was not found in the database. "
                "A new model will be added."
            )

            modelID, _ = db.insertItemsTable(
                query="""
                    INSERT INTO Model
                    (
                        ModelName,
                        TrainingStatus,
                        CreatedAt
                    )
                    VALUES (?, ?, ?)
                """,
                values=(
                    clientAnswer["ModelName"],
                    "Training",
                    datetime.now().isoformat()
                )
            )

        # --------------------------------------------------
        # Determine next version for this model
        # --------------------------------------------------

        versionInfo = db.fetchInfo(
            """
            SELECT
                MAX(ModelVersion) AS MaximumVersion
            FROM ModelVersion
            WHERE ModelID = ?
            """,
            (
                modelID,
            )
        )

        newModelVersion = (
            versionInfo[0]["MaximumVersion"] + 1
            if versionInfo
            and versionInfo[0]["MaximumVersion"] is not None
            else 1
        )

        # --------------------------------------------------
        # Create model
        # --------------------------------------------------

        modelToBeTrained = ModelFactory().createModel(
            modelName=clientAnswer["ModelName"],
            numClasses=clientAnswer["NumClasses"]
        )

        # --------------------------------------------------
        # Sample dataset
        # --------------------------------------------------

        sampledDatasets = datasetSampling(
            clientAnswer=clientAnswer,
            dbFile=dbFile
        )

        # --------------------------------------------------
        # Build TensorFlow datasets
        # --------------------------------------------------

        trainDataset = buildTrainingDataset(
            records=sampledDatasets["trainingRecords"],
            batchSize=clientAnswer["BatchSize"]
        )

        validationDataset = buildTrainingDataset(
            records=sampledDatasets["validationRecords"],
            batchSize=clientAnswer["BatchSize"],
            shuffle=False
        )

        # --------------------------------------------------
        # Model checkpoint
        # --------------------------------------------------

        filePath = (
            f"{clientAnswer['ModelName']}"
            f"_version_{newModelVersion}.keras"
        )

        checkPoint = keras.callbacks.ModelCheckpoint(
            filepath=filePath,
            monitor="val_loss",
            save_best_only=True
        )

        # --------------------------------------------------
        # Train model
        # --------------------------------------------------

        history = modelToBeTrained.trainModel(
            trainDataset=trainDataset,
            valDataset=validationDataset,
            epochs=clientAnswer["Epochs"],
            checkpoint=checkPoint
        )

        # --------------------------------------------------
        # Store ModelWeights
        # --------------------------------------------------

        modelWeightsID, _ = db.insertItemsTable(
            query="""
                INSERT INTO ModelWeights
                (
                    ModelWeightsPath
                )
                VALUES (?)
            """,
            values=(
                filePath,
            )
        )

        # --------------------------------------------------
        # Store Hyperparameters
        # --------------------------------------------------

        hyperparameterID, _ = db.insertItemsTable(
            query="""
                INSERT INTO Hyperparameter
                (
                    Hyperparameters
                )
                VALUES (?)
            """,
            values=(
                str({
                    "LearningRate":
                        clientAnswer["LearningRate"],

                    "BatchSize":
                        clientAnswer["BatchSize"],

                    "Epochs":
                        clientAnswer["Epochs"]
                }),
            )
        )

        # --------------------------------------------------
        # Store Metrics
        # --------------------------------------------------

        metricID, _ = db.insertItemsTable(
            query="""
                INSERT INTO ModelMetric
                (
                    MSE,
                    r2,
                    loss
                )
                VALUES (?, ?, ?)
            """,
            values=(
                history.history["mse"][-1],
                history.history.get(
                    "accuracy",
                    [None]
                )[-1],
                history.history["loss"][-1]
            )
        )

        # --------------------------------------------------
        # Store ModelVersion
        # --------------------------------------------------

        modelVersionID, _ = db.insertItemsTable(
            query="""
                INSERT INTO ModelVersion
                (
                    ModelID,
                    ModelVersion,
                    CreatedAt,
                    ModelMetricID,
                    HyperparameterID,
                    ModelWeightsID
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            values=(
                modelID,
                newModelVersion,
                datetime.now().isoformat(),
                metricID,
                hyperparameterID,
                modelWeightsID
            )
        )

        # --------------------------------------------------
        # Update model status
        # --------------------------------------------------

        db.updateItem(
            updateStatement="""
                UPDATE Model
                SET
                    TrainingStatus = ?,
                    CreatedAt = ?
                WHERE ModelID = ?
            """,
            Values=(
                "Finalized",
                datetime.now().isoformat(),
                modelID
            )
        )

        # --------------------------------------------------
        # Store DatasetSplit TRAIN
        # --------------------------------------------------

        for tile in sampledDatasets["trainingTiles"]:

            db.insertItemsTable(
                query="""
                    INSERT INTO DatasetSplit
                    (
                        ModelVersionID,
                        DatasetID,
                        PreprocessingID,
                        SplitType
                    )
                    VALUES (?, ?, ?, ?)
                """,
                values=(
                    modelVersionID,
                    clientAnswer["DatasetID"],
                    tile["PreprocessingID"],
                    "TRAIN"
                )
            )

        # --------------------------------------------------
        # Store DatasetSplit VALIDATION
        # --------------------------------------------------

        for tile in sampledDatasets["validationTiles"]:

            db.insertItemsTable(
                query="""
                    INSERT INTO DatasetSplit
                    (
                        ModelVersionID,
                        DatasetID,
                        PreprocessingID,
                        SplitType
                    )
                    VALUES (?, ?, ?, ?)
                """,
                values=(
                    modelVersionID,
                    clientAnswer["DatasetID"],
                    tile["PreprocessingID"],
                    "VALIDATION"
                )
            )

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        return {
            "ModelID": modelID,
            "ModelVersionID": modelVersionID,
            "ModelVersion": newModelVersion,
            "DatasetID": clientAnswer["DatasetID"],
            "Status": "Completed",
            "TrainingTiles": len(
                sampledDatasets["trainingTiles"]
            ),
            "ValidationTiles": len(
                sampledDatasets["validationTiles"]
            )
        }

    finally:

        db.closeConnection()

  
# defines the fuction to train several models
def trainSeveralModels(clientAnswer:list[dict])->list[dict]:

   # loops through the list of dictionaries to train the models in the list
   for answer in clientAnswer:

    # trains a model at the time
    results=trainModel(clientAnswer=answer)

    # returns last results
    return results

# defines the fuction to train all the models
def trainAllModels(clientAnswer:dict, dbFile:str)->None:

    # gets the name of all the available models
    modelNames=ModelTable(dbFile=dbFile).fetchInfo(statement="FROM Model SELECT ModelName")

    # loops through all the models available and execute the function train model
    for name in modelNames[0]:

        # adds the ModelName key to dictionary
        clientAnswer['ModelName']=name.get('ModelName') 

        # executes the function train model and get the results
        results=trainModel(clientAnswer=clientAnswer)
    
    # returns the last results
    return results
