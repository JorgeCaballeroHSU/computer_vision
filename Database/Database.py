# this files contains the classses for the creation, modification and deletion of the database and its tables

# import required libraries
import sqlite3
from sqlite3 import Error


class Database:
    
    # Class' properties
    _filePath:str=''
    
    def __init__(self, dbFile: str)->None:
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        # initialize the connection variable to None
        self._filePath=dbFile

        #return nothing
        return None

    # inserts new items in a table
    def insertItemsTable(self, query: str, values: tuple = ()) -> tuple:
        """ Safely insert data into a table using parameterized queries.

        :param query: SQL INSERT statement with placeholders (?)
        :param values: tuple of values to insert """ 

        try:

            cursor=self.conn.cursor()

            # execute parameterized query
            cursor.execute(query, values)

            # commit changes
            self.conn.commit()

            # gets the last rowID and the row count
            return (cursor.lastrowid, cursor.rowcount)


        # catches errors during execution
        except Error as e:

            # prints errors
            print(f"Error inserting data: {e}")

            # rolls back to previous state
            self.conn.rollback()

            # gets the last rowID and the row count
            return (-1,-1)

    
    # module to fetch information from the database
    def fetchInfo(self,statement:str)-> list:

        # initializes the variable
        fetchedElement=()

        # opens a try block to cath errors
        try:

            # fetches the elements indicated by the statement
            fetchedElement=self.conn.cursor().execute(statement).fetchall()
            
            # returns fetched elements
            return  [dict(row) for row in fetchedElement] # returns the fetched elements as a list of dictionaries

        # catches errors during execution
        except Error as e:

            # prints the error found
            print(f'Error fetching data: {e}')

            # returns empty list
            return []
        
    
    # module to update an existing element
    def updateItem(self, updateStatement:str, Values:tuple)->tuple:

        # opens try block to catch errors
        try:

            cursor=self.conn.cursor()

            # executes the given statement
            cursor.execute(updateStatement,Values)

            # commits executed statement
            self.conn.commit()

            # gets the last rowID and the row count
            return(-1, cursor.rowcount)

        # catches errors during execution
        except Error as e:

            # prints the error found
            print(f'Error updating data: {e}')

            # rolls back to previous state
            self.conn.rollback()

            # gets the last rowID and the row count
            return (-1,-1)


    # module to open connection to the database
    def openConnection(self)->None:

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            self.conn = sqlite3.connect(self._filePath)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.conn.row_factory = sqlite3.Row

        # catches any errors that occur during the connection process and print the error message
        except Error as e:
            print(e)

        # returns none
        return None

    # module to close connections to the database
    def closeConnection(self)->None:
        """ close the database connection
        """
        if self.conn:
            self.conn.close()
            self.conn=None

        # return nothing
        return None
    
# class to create the tables
class Schema():

    # creates the tables in the database
    # creates all the tables necessary for running this project. The database table relations can be seen in the document
    # Datenbak - Class Diagram.png
    @staticmethod
    def TableSchemaRawData()->list:
        """ create a table from the create_table_sql statement
        :return: list of SQL statements for creating tables 
        """
        # defines the sql-command for the creation of the table Dataset
        dataset="CREATE TABLE IF NOT EXISTS Dataset (datasetID INTEGER PRIMARY KEY, ProjectName TEXT NOT NULL, MaterialType TEXT NOT NULL,"\
        "created DATE, description TEXT NOT NULL);"

        # defines the sql-command for the creation of the table CameraInfo
        cameraInfo= "CREATE TABLE IF NOT EXISTS CameraInfo (CameraInfoID INTEGER PRIMARY KEY, Manufacturer TEXT NOT NULL," \
        "CameraModel TEXT NOT NULL, ISO TEXT NOT NULL, Focus TEXT NOT NULL, ExposureTime TEXT NOT NULL, FlashMode TEXT NOT NULL,"\
        "FocalLength INTEGER NOT NULL, Objective TEXT NOT NULL, Extension TEXT NOT NULL);"

        # defines the table for the creation of the table Sample
        sample="CREATE TABLE IF NOT EXISTS Sample (SampleID INTEGER PRIMARY KEY, " \
        "Label TEXT NOT NULL, filePath TEXT NOT NULL, FilePath TEXT NOT NULL," \
        "CaptureTime DATE NOT NULL, CameraInfoID INTEGER NOT NULL," \
        "DatasetID INTEGER NOT NULL, MaterialID INTEGER NOT NULL, " \
        "FOREIGN KEY(CameraInfoID) REFERENCES CameraInfo(CameraInfoID)," \
        "FOREIGN KEY(DatasetID) REFERENCES Dataset(datasetID)," \
        "FOREIGN KEY(MaterialID) REFERENCES MaterialType(MaterialTypeID) ON DELETE CASCADE ON UPDATE CASCADE)," \
        "FOREIGN KEY(JunctionPreID) REFERENCES JunctionPre(JunctionPreID) ON DELETE CASCADE ON UPDATE CASCADE);"
        
        # defines the sql-command for the creation of the table MaterialType
        materialType="CREATE TABLE IF NOT EXISTS MaterialType (MaterialTypeID INTEGER PRIMARY KEY, mm0063 REAL, " \
        "mm0125 REAL, mm0250 REAL, mm0400 REAL, mm0500 REAL, mm1000 REAL, mm2000 REAL, mm4000 REAL," \
        "mm8000 REAL, mm1600 REAL, mm3200 REAL);"

        # gets all the variables in one place to execute them
        tables = [
             sample, cameraInfo, dataset, materialType
            ]
        
        # returns the list of tables to be created
        return tables
    
    @staticmethod
    def TableSchemaDerivedArtifacts()->list:
        """ create a table from the create_table_sql statement
        :return: list of SQL statements for creating tables
        """
        # defines the sql-command for the creation of the table JunctionPre
        JunctionPre="CREATE TABLE IF NOT EXISTS JunctionPre (JunctionPreID INTEGER PRIMARY KEY, SampleID INTEGER, PreprocessingID INTERGER, " \
        "FOREIGN KEY(PreprocessingID) REFERENCES Preprocessing(PreprocessingID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql- statement for the creation of the table Preprocessing
        Preprocessing="CREATE TABLE IF NOT EXISTS Preprocessing (PreprocessingID INTEGER PRIMARY KEY, PreprocessingType TEXT NOT NULL, " \
        "FilePath TEXT NOT NULL, Label TEXT NOT NULL);" \
        
        # defines the sql- statement for the creation of the table JunctionAugmentation
        JunctionAugmentation="CREATE TABLE IF NOT EXISTS JunctionAugmentation (JunctionAugID INTEGER PRIMARY KEY, PreprocessingID INTEGER, AugmentationID INTEGER, " \
        "FOREIGN KEY(PreprocessingID) REFERENCES Preprocessing(PreprocessingID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(AugmentationID) REFERENCES Augmentation(AugmentationID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table Augmentation
        augmentation=" CREATE TABLE IF NOT EXISTS Augmentation (AugmentationID INTEGER PRIMARY KEY, Method TEXT NOT NULL, " \
        "FilePath TEXT NOT NULL);" \

        # defines the sql-command for the creation of the table TFRecording
        TFRecording="CREATE TABLE IF NOT EXISTS TFRecording (TFRecordingID INTEGER PRIMARY KEY, Label TEXT NOT NULL, FilePath TEXT NOT NULL, AugmentationID INTEGER," \
        "FOREIGN KEY(AugmentationID) REFERENCES Augmentation(AugmentationID) ON DELETE CASCADE ON UPDATE CASCADE);"
        
        # returns the list of tables to be created
        return [JunctionPre, Preprocessing, JunctionAugmentation, augmentation, TFRecording]

    @staticmethod
    def TableSchemaModel()->list:
        """ create a table from the create_table_sql statement
        :return: list of SQL statements for creating tables
        """
        # defines the sql-statement for the creation of the table Validation
        validation="CREATE TABLE IF NOT EXISTS Validation (ValidationID INTEGER PRIMARY KEY, TFRecordingID INTEGER, ModelID INTEGER, " \
        "FOREIGN KEY(TFRecordingID) REFERENCES TFRecording(TFRecordingID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(ModelID) REFERENCES Model(ModelID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-Statement for the creation of the table Testing
        testing="CREATE TABLE IF NOT EXISTS Testing (TestingID INTEGER PRIMARY KEY, TFRecordingID INTEGER, ModelID INTEGER, " \
        "FOREIGN KEY(TFRecordingID) REFERENCES TFRecording(TFRecordingID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(ModelID) REFERENCES Model(ModelID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-Statement for the creation of the table Training
        training="CREATE TABLE IF NOT EXISTS Training (TrainingID INTEGER PRIMARY KEY, TFRecordingID INTEGER, ModelID INTEGER, " \
        "FOREIGN KEY(TFRecordingID) REFERENCES TFRecording(TFRecordingID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(ModelID) REFERENCES Model(ModelID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table Model
        model= "CREATE TABLE IF NOT EXISTS Model (ModelID INTEGER PRIMARY KEY, ModelName TEXT NOT NULL, TrainingStatus TEXT NOT NULL, " \
        "CreatedAt DATE NOT NULL, ModelVersionID INTEGER, " \
        "FOREIGN KEY (ModelVersionID) REFERENCES ModelVersion(ModelVersionID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table ModelVersion
        modelVersion="CREATE TABLE IF NOT EXISTS ModelVersion (ModelVersionID INTEGER PRIMARY KEY, ModelVersion INTEGER NOT NULL, CreatedAt DATE NOT NULL, " \
        "ModelMetricID INTEGER, HyperparameterID INTEGER, ModelWeightsID INTEGER, " \
        "FOREIGN KEY (ModelMetricID) REFERENCES ModelMetric(ModelMetricID) ON DELETE CASCADE ON UPDATE CASCADE)" \
        "FOREIGN KEY (HyperparameterID) REFERENCES Hyperparameter(HyperparameterID) ON DELETE CASCADE ON UPDATE CASCADE)" \
        "FOREIGN KEY (ModelWeightsID) REFERENCES ModelWeights(ModelWeightsID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table ModelMetric
        modelMetric="CREATE TABLE IF NOT EXISTS ModelMetric (ModelMetricID INTEGER PRIMARY KEY, MSE REAL, r2 REAL, " \
        "loss REAL);"

        # defines the sql-command for the creation of the table Hyperparameter
        Hyperparameter= "CREATE TABLE IF NOT EXISTS Hyperparameter (HyperparameterID INTEGER PRIMARY KEY, Hyperparameters TEXT);"

        # defines the sql-command for the creation of the table ModelWeights
        modelWeights= "CREATE TABLE IF NOT EXISTS ModelWeights(ModelWeightsID INTEGER PRIMARY KEY, ModelWeightsPath TEXT);"

        # returns the list of tables to be created
        return [modelMetric, Hyperparameter, modelWeights, model, modelVersion]

    

# class to check if the data to be added to the database already exists in the database.
class DataChecker(Database):

    # checks if the data to be added to the database already exists in the database
    def checkData(self, query: str, values: tuple = ()) -> bool:
        """ Safely check if data exists in a table using parameterized queries.

        :param query: SQL SELECT statement with placeholders (?)
        :param values: tuple of values to check
        :return: True if data exists, False otherwise """ 

        try:
            # open connection
            self.openConnection()

            cursor=self.conn.cursor()

            # execute parameterized query
            cursor.execute(query, values)

            # fetch one result
            result = cursor.fetchone()

            # return True if result is not None, False otherwise
            return result is not None

        # catches errors during execution
        except Error as e:

            # prints errors
            print(f"Error checking data: {e}")

            # rolls back to previous state
            self.conn.rollback()

            return False

        finally:

            # always close connection
            self.closeConnection()


# class for table Label.
class LabelTable (Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # updates the database with the metadata and the location of the image
    def insertLabelTable(self, clientAnswer:dict, labelFile:str)->int:
        
        # inserts the database's table with the metadata and image location
        # inserts table label
        lastRowID,=self.insertItemsTable( # this has to check if the label type already exists in the database, if it already exists, there is no need to add a thing.
            query='''INSERT INTO label (name, labelType) VALUES (?, ?) ''',
            values=(labelFile,                      # labelfile is the label of the picture.
                    clientAnswer.get('labelType'))      # LabelType corresponds to the type of label. S, K, T or M
        )

        # returns the last id of the Label table.
        return lastRowID

# class for the table CameraInfo
class CameraInfoTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the cameraInfo table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertCameraInfoTable(self, clientAnswer:dict)->int:

        # inserts the cameraInfo table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(# correct<<<-------
            query='''INSERT INTO cameraInfo (Manufacturer, CameraModel, ISO, Focus, Exposuretime, FlashMode, FocalLength, Objective, Extension) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
            values=(clientAnswer.get('Manufacturer'),       # Manufacturer corresponds to the manufacturer of the camera used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('CameraModel'),        # CameraModel corresponds to the model of the camera used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('ISO'),                # ISO corresponds to the ISO used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('Focus'),              # Focus corresponds to the focus used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('Exposuretime'),       # Exposuretime corresponds to the exposure time used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('FlashMode'),          # FlashMode corresponds to the flash mode used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('FocalLength'),        # FocalLength corresponds to the focal length used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('Objective'),          # Objective corresponds to the objective used to take the picture. It is obtained from the exif data of the picture.
                    clientAnswer.get('Extension'))          # Extension corresponds to the extension used to take the picture. It is obtained fromthe exif data ofthe picture.
        )

        # returns the last id of the CameraInfo table.
        return lastRowID

# class for the table Dataset
class DatasetTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Dataset table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertDatasetTable(self, clientAnswer:dict, labelFile:str)->int:

        # inserts the Dataset table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Dataset (name, ProjectName, Created, Description) VALUES (?, ?, ?, ?) ''',
            values=(labelFile, clientAnswer.get('ProjectName'), clientAnswer.get('Created'), clientAnswer.get('Description'))
        )

        # returns the last id of the Dataset table.
        return lastRowID

# class for the table MatrialType
class MaterialTypeTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the MaterialType table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertMaterialTypeTable(self, clientAnswer:dict)->int:
        # inserts the MaterialType table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO MaterialType (mm0063, mm0125, mm0250, mm0400, mm0500, mm1000, mm2000, mm4000, mm8000, mm1600, mm3200) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
            values=(
                clientAnswer.get('mm0063'),                 # mm0063 corresponds to the value of the material type for the size of 0.063 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm0125'),                 # mm0125 corresponds to the value of the material type for the size of 0.125 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm0250'),                 # mm0250 corresponds to the value of the material type for the size of 0.250 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm0400'),                 # mm0400 corresponds to the value of the material type for the size of 0.400 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm0500'),                 # mm0500 corresponds to the value of the material type for the size of 0.500 mm. It is obtained from the exif data of the picture.  
                clientAnswer.get('mm1000'),                 # mm1000 corresponds to the value of the material type for the size of 1.000 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm2000'),                 # mm2000 corresponds to the value of the material type for the size of 2.000 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm4000'),                 # mm4000 corresponds to the value of the material type for the size of 4.000 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm8000'),                 # mm8000 corresponds to the value of the material type for the size of 8.000 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm1600'),                 # mm1600 corresponds to the value of the material type for the size of 16.000 mm. It is obtained from the exif data of the picture.
                clientAnswer.get('mm3200'))                 # mm3200 corresponds to the value of the material type for the size of 32.000 mm. It is obtained from the exif data of the picture.
        )

        # returns the last id of the MaterialType table.
        return lastRowID
    
# class for the sample Table manipualtion
class SampleTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # updates table sample 
    def insertSampleTable(self, clientAnswer:dict, isProcessed:bool,LastCameraID:int,LastDatasetID:int,LastMaterialID:int,LastTFRLabelID:int)->int:

        # updates table sample  
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Sample (filePath, captureTime, isProcessed, CameraID, DatasetID, MaterialID, IDTFL) VALUES (?, ?, ?, ?, ?, ?, ?) ''',
            values=(
                clientAnswer.get('filePath'),               # filePath corresponds to the file path of the picture. It is obtained from the exif data of the picture.
                clientAnswer.get('captureTime'),            # captureTime corresponds to the capture time of the picture. It is obtained from the exif data of the picture.
                isProcessed,                                # isProcessed corresponds to whether the picture has been processed or not. It is set to 0 when the picture is added to the database and it is set to 1 when the picture has been processed.
                LastCameraID,                               # CameraID corresponds to the ID of the camera used to take the picture. It is obtained from the exif data of the picture.
                LastDatasetID,                               # DatasetID corresponds to the ID of the dataset to which the picture belongs. It is obtained from the exif data of the picture.
                LastMaterialID,                             # MaterialID corresponds to the ID of the material type of the picture. It is obtained from the exif data of the picture.
                LastTFRLabelID                               # IDTFL corresponds to the ID of the TFRLabel of the picture. It is obtained from the exif data of the picture.
            )
        )

        # returns the last id of the Sample table.
        return lastRowID

# class for the table Augmentation
class AugmentationTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # updates table Augmentation
    def insertAugmentationTable(self, method:str, SampleID:int)->int:
        # possible methods for augmentation: rotation (R), flipping(F), color jittering(C), translation(T), none(N).

        # updates table Augmentation
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Augmentation (method, SampleID) VALUES (?, ?) ''',
            values=(
                method,                                     # method corresponds to the augmentation method used to augment the picture. It is obtained from the exif data of the picture.
                SampleID                                    # SampleID corresponds to the ID of the sample to which the augmentation belongs. It is obtained from the exif data of the picture.
            )
        )

        # returns the last row ID
        return lastRowID

# class for TFrecording
class TFRecordingTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # updates table TFRecording
    def insertTFRecordingTable(self, TFRecord:bytes, IDTFL:int)->None:

        # updates table TFRecording
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO TFRecording (TFRecording, IDTFL) VALUES (?, ?) ''',
            values=(
                TFRecord,                                  # TFRecord corresponds to the binary of the TFRecord created with the picture. It is obtained from the exif data of the picture.
                IDTFL                                      # IDTFL corresponds to the ID of the TFRLabel of the picture. It is obtained from the exif data of the picture.
            )
        )

        # returns the last row ID
        return lastRowID
    
# class for the TFRLabel table
class TFRLabelTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # updates table TFRLabel
    def insertTFRLabelTable(self, sampleID:int, IDTFR:int)->int:

        # updates table TFRLabel
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO TFRLabel (sampleID, IDTFR) VALUES (?, ?) ''',
            values=(
                sampleID,                                   # sampleID corresponds to the ID of the sample to which the TFRLabel belongs. It is obtained from the exif data of the picture.
                IDTFR                                       # IDTFR corresponds to the ID of the TFRecord of the picture. It is obtained from the exif data of the picture.
            )
        )

        # returns the last row ID
        return lastRowID
    