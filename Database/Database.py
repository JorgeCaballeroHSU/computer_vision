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
class Schema(Database):

    # creates the tables in the database
    # creates all the tables necessary for running this project. The database table relations can be seen in the document
    # Datenbak - Class Diagram.png
     
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

        # creates the tables in the database
        self.__createTables(self.TableSchemaRawData())
        self.__createTables(self.TableSchemaDerivedArtifacts())
        self.__createTables(self.TableSchemaModel())

    # creates the tables in the database
    def __createTables(self, tableStatements:list)->None:
        """ create tables in the database using the provided SQL statements
        :param tableStatements: list of SQL statements for creating tables
        """
        # opens a try block to catch errors
        try:

            # creates a cursor object to execute SQL statements
            cursor=self.conn.cursor()

            # executes each statement in the provided list of table creation statements
            for statement in tableStatements:
                cursor.execute(statement)

            # commits changes to the database
            self.conn.commit()

        # catches any errors that occur during the table creation process and print the error message
        except Error as e:
            print(f"Error creating tables: {e}")

        # returns none
        return None

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
        "Label TEXT NOT NULL,  FilePath TEXT NOT NULL," \
        "CaptureTime DATE NOT NULL, CameraInfoID INTEGER NOT NULL," \
        "DatasetID INTEGER NOT NULL, MaterialType INTEGER NOT NULL, JunctionPreID INTEGER," \
        "FOREIGN KEY(CameraInfoID) REFERENCES CameraInfo(CameraInfoID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(DatasetID) REFERENCES Dataset(datasetID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(MaterialType) REFERENCES MaterialType(MaterialTypeID) ON DELETE CASCADE ON UPDATE CASCADE," \
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
        JunctionPre="CREATE TABLE IF NOT EXISTS JunctionPre (JunctionPreID INTEGER PRIMARY KEY, SampleID INTEGER, PreprocessingID INTEGER, " \
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
        "FOREIGN KEY (ModelMetricID) REFERENCES ModelMetric(ModelMetricID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY (HyperparameterID) REFERENCES Hyperparameter(HyperparameterID) ON DELETE CASCADE ON UPDATE CASCADE," \
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
    
        # updates the a parameter of the CameraInfo table
    def updateCameraInfoTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE CameraInfo SET Manufacturer=?, CameraModel=?, ISO=?, Focus=?, Exposuretime=?, /"
        "FlashMode=?,FocalLength=?,Objective=?,Extension=? WHERE CameraInfoID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['Manufacturer'],
            clientAnswer['CameraModel'],
            clientAnswer['ISO'],
            clientAnswer['Focus'],
            clientAnswer['Exposuretime'],
            clientAnswer['FlashMode'],
            clientAnswer['FocalLength'],
            clientAnswer['Objective'],
            clientAnswer['Extension'],
            clientAnswer['CameraInfoID']
        ))

        # returns None
        return None
    
    # deletes the defined CameraInfo row
    def deleteCameraInfoTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeCameraInfoTable='DELETE FROM CameraInfo WHERE CameraInfoID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeCameraInfoTable,Values=(clientAnswer['CameraInfoID'],))

        return None
    
    # fetchs the database in the CameraInfo table
    def fetchCameraInfo(self)-> dict:

        # fetches the dataset from the database
        dataset=self.fetchInfo(query='''SELECT * FROM CameraInfo''')

        # returns the dataset
        return dataset

# class for the table Dataset
class DatasetTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Dataset table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertDatasetTable(self, clientAnswer:dict)->int:

        # inserts the Dataset table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Dataset (ProjectName, MaterialType, Created, Description) VALUES (?, ?, ?, ?) ''',
            values=(clientAnswer.get('ProjectName'), clientAnswer.get('MaterialType'), clientAnswer.get('Created'), clientAnswer.get('Description'))
        )

        # returns the last id of the Dataset table.
        return lastRowID
    
    # updates the a parameter of the Dataset table
    def updateDatasetTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Dataset SET ProjectName=?, MaterialType=?, Created=?, Description=? WHERE DatasetID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['ProjectName'],
            clientAnswer['MaterialType'],
            clientAnswer['Created'],
            clientAnswer['Description'],
            clientAnswer['DatasetID']
        ))

        # returns None
        return None
    
    # deletes the defined dataset row
    def deleteDatasetTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Dataset WHERE DatasetID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['DatasetID'],))

        return None

    # fetchs the database in te table Dataset
    def fetchDataset(self)-> dict:

        # fetches the dataset from the database
        dataset=self.fetchInfo(query='''SELECT * FROM Dataset''')

        # returns the dataset
        return dataset
    

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
    
    # updates the a parameter of the MaterialType table
    def updateMaterialTypeTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE MaterialType SET mm0063=?, mm0125=?, mm0250=?, mm0400=?, "\
        "mm0500=?, mm1000=?, mm2000=?, mm4000=?, mm8000=?, mm1600=?, mm3200=? WHERE MaterialTypeID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['mm0063'],
            clientAnswer['mm0125'],
            clientAnswer['mm0250'],
            clientAnswer['mm0400'],
            clientAnswer['mm0500'],
            clientAnswer['mm1000'],
            clientAnswer['mm2000'],
            clientAnswer['mm4000'],
            clientAnswer['mm8000'],
            clientAnswer['mm1600'],
            clientAnswer['mm3200'],
            clientAnswer['MaterialTypeID']
        ))

        # returns None
        return None
    
    # deletes the defined dataset row
    def deleteMaterialTypeTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM MaterialType WHERE MaterialTypeID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['MaterialTypeID'],))

        return None
    
    # fetches the materialType from the database
    def fetchMaterialType(self)-> dict:

        # fetches the materialType from the database
        materialType=self.fetchInfo(query='''SELECT * FROM MaterialType''')

        # returns the materialType
        return materialType
    
    
# class for the sample Table manipualtion
class SampleTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the sample table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertSampleTable(self, clientAnswer:dict)->int:
        # inserts the sample table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Sample (Label, FilePath, CaptureTime, CameraInfoID, DatasetID, MaterialTypeID) VALUES (?, ?, ?, ?, ?, ?) ''',
            values=(clientAnswer.get('Label'), clientAnswer.get('FilePath'), clientAnswer.get('CaptureTime'), 
                    clientAnswer.get('cameraInfoID'), clientAnswer.get('datasetID'), clientAnswer.get('materialTypeID'))
        )

        # returns the last id of the sample table.
        return lastRowID
    
        # updates a JunctionAugmentation row
    def updateJunctionAugmentationTable(self, clientAnswer: dict) -> None:
        statement = '''
        UPDATE JunctionAugmentation 
        SET PreprocessingID = ?, AugmentationID = ?
        WHERE JunctionAugID = ?
        '''

        self.updateItem(
            updateStatement=statement,
            Values=(
                clientAnswer['PreprocessingID'],
                clientAnswer['AugmentationID'],
                clientAnswer['JunctionAugID']
            )
        )
        return None

    # deletes a JunctionAugmentation row
    def deleteJunctionAugmentationTable(self, clientAnswer: dict) -> None:
        statement = 'DELETE FROM JunctionAugmentation WHERE JunctionAugID = ?'

        self.updateItem(
            updateStatement=statement,
            Values=(clientAnswer['JunctionAugID'],)
        )
        return None

    # fetches all JunctionAugmentation rows
    def fetchJunctionAugmentation(self) -> dict:
        junctionAugmentation = self.fetchInfo(
            query='''SELECT * FROM JunctionAugmentation'''
        )
        return junctionAugmentation
    
# class for the table JunctionPre
class JunctionPreTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the JunctionPre table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertJunctionPreTable(self, clientAnswer:dict)->int:
        # inserts the JunctionPre table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO JunctionPre (SampleID, PreprocessingID) VALUES (?, ?) ''',
            values=(clientAnswer['SampleID'], clientAnswer['PreprocessingID'])
        )

        # returns the last id of the JunctionPre table.
        return lastRowID
    
    # updates the a parameter of the JunctionPre table
    def updateJunctionPreTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE JunctionPre SET SampleID=?, PreprocessingID=? WHERE JunctionPreID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['SampleID'],
            clientAnswer['PreprocessingID'],
            clientAnswer['JunctionPreID']
        ))

        # returns None
        return None
    
    # deletes the defined JunctionPre row
    def deleteJunctionPreTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM JunctionPre WHERE JunctionPreID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['JunctionPreID'],))

        return None
    
    # fetches the JunctionPre from the database
    def fetchJunctionPre(self)-> dict:

        # fetches the JunctionPre from the database
        junctionPre=self.fetchInfo(query='''SELECT * FROM JunctionPre''')

        # returns the JunctionPre
        return junctionPre
    
# class for the table Preprocessing
class PreprocessingTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Preprocessing table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertPreprocessingTable(self, clientAnswer:dict)->int:
        # inserts the Preprocessing table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Preprocessing (PreprocessingType, FilePath, Label) VALUES (?, ?, ?) ''',
            values=(clientAnswer.get('PreprocessingType'), clientAnswer.get('FilePath'), clientAnswer.get('Label'))
        )

        # returns the last id of the Preprocessing table.
        return lastRowID
    
        # updates the a parameter of the Preprocessing table
    def updatePreprocessingTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Preprocessing SET PreprocessingType=?, FilePath=?, Label=? WHERE PreprocessingID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['PreprocessingType'],
            clientAnswer['FilePath'],
            clientAnswer['Label'],
            clientAnswer['PreprocessingID']
        ))

        # returns None
        return None
    
    # deletes the defined Preprocessing row
    def deletePreprocessingTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Preprocessing WHERE PreprocessingID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['PreprocessingID'],))

        return None
    
    
    # fetches the Preprocessing from the database
    def fetchPreprocessing(self)-> dict:

        # fetches the Preprocessing from the database
        preprocessing=self.fetchInfo(query='''SELECT * FROM Preprocessing''')

        # returns the Preprocessing
        return preprocessing
    
# class for the table JunctionAugmentation
class JunctionAugmentationTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the JunctionAugmentation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertJunctionAugmentationTable(self, clientAnswer:dict)->int:
        # inserts the JunctionAugmentation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO JunctionAugmentation (PreprocessingID, AugmentationID) VALUES (?, ?) ''',
            values=(clientAnswer['PreprocessingID'],  clientAnswer['AugmentationID'])
        )

        # returns the last id of the JunctionAugmentation table.
        return lastRowID
    
    # updates the a parameter of the JunctionAugmentation table
    def updateJunctionAugmentationTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE JunctionAugmentation SET PreprocessingID=?, AugmentationID=?, WHERE JunctionAugmentationID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['PreprocessingID'],
            clientAnswer['AugmentationID'],
            clientAnswer['JunctionAugmentationID']
        ))

        # returns None
        return None
    
    # deletes the defined JunctionAugmentation row
    def deleteJunctionAugmentationTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM JunctionAugmentation WHERE JunctionAugmentationID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['JunctionAugmentationID'],))

        return None
    
    # fetches the JunctionAugmentation from the database
    def fetchJunctionAugmentation(self)-> dict:

        # fetches the JunctionAugmentation from the database
        junctionAugmentation=self.fetchInfo(query='''SELECT * FROM JunctionAugmentation''')

        # returns the JunctionAugmentation
        return junctionAugmentation
    
    
# class for the table Augmentation
class AugmentationTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Augmentation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertAugmentationTable(self, clientAnswer:dict)->int:
        # inserts the Augmentation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Augmentation (Method, FilePath) VALUES (?, ?) ''',
            values=(clientAnswer.get('Method'), clientAnswer.get('FilePath'))
        )

        # returns the last id of the Augmentation table.
        return lastRowID
    
    # updates the a parameter of the Augmentation table
    def updateAugmentationTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Augmentation SET Method=?, FilePath=?, WHERE AugmentationID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['Method'],
            clientAnswer['FilePath'],
            clientAnswer['AugmentationID']
        ))

        # returns None
        return None
    
    # deletes the defined Augmentation row
    def deleteAugmentationTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Augmentation WHERE AugmentationID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['AugmentationID'],))

        return None
    
    # fetches the Augmentation from the database
    def fetchAugmentation(self)-> dict:

        # fetches the Augmentation from the database
        augmentation=self.fetchInfo(query='''SELECT * FROM Augmentation''')

        # returns the Augmentation
        return augmentation
    
# class for the table TFRecording
class TFRecordingTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the TFRecording table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertTFRecordingTable(self, clientAnswer:dict)->int:
        # inserts the TFRecording table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO TFRecording (Label, FilePath, AugmentationID) VALUES (?, ?, ?) ''',
            values=(clientAnswer.get('Label'), clientAnswer.get('FilePath'), clientAnswer.get('AugmentationID'))
        )

    # updates the a parameter of the TFRecording table
    def updateTFRecordingTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE TFRecording SET Label=?, FilePath=?, AugmentationID=? WHERE TFRecordingID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['Label'],
            clientAnswer['FilePath'],
            clientAnswer['AugmentationID'],
            clientAnswer['TFRecordingID']
        ))

        # returns None
        return None
    
    # deletes the defined TFRecording row
    def deleteTFRecordingTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM TFRecording WHERE TFRecordingID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['TFRecordingID'],))

        return None
    
    # fetcehes the TFRecording from the database
    def fetchTFRecording(self)-> dict:

        # fetches the TFRecording from the database
        tfRecording=self.fetchInfo(query='''SELECT * FROM TFRecording''')

        # returns the TFRecording
        return tfRecording
    
# class for the table Validation
class ValidationTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Validation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertValidationTable(self, clientAnswer:dict)->int:
        # inserts the Validation table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Validation (TFRecordingID, ModelID) VALUES (?, ?) ''',
            values=(clientAnswer['TFRecordingID'], clientAnswer['ModelID'])
        )

        # returns the last id of the Validation table.
        return lastRowID
    
    # updates the a parameter of the Validation table
    def updateValidationTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Validation SET TFRecordingID=?, ModelID=? WHERE ValidationID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['TFRecordingID'],
            clientAnswer['ModelID'],
            clientAnswer['ValidationID']
        ))

        # returns None
        return None
    
    # deletes the defined Validation row
    def deleteValidationTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Validation WHERE ValidationID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['ValidationID'],))

        return None
    
    # fetches the Validation from the database
    def fetchValidation(self)-> dict:

        # fetches the Validation from the database
        validation=self.fetchInfo(query='''SELECT * FROM Validation''')

        # returns the Validation
        return validation
    
# class for the table Testing
class TestingTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Testing table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertTestingTable(self, clientAnswer)->int:
        # inserts the Testing table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Testing (TFRecordingID, ModelID) VALUES (?, ?) ''',
            values=(clientAnswer['TFRecordingID'], clientAnswer['ModelID'])
        )

        # returns the last id of the Testing table.
        return lastRowID
    
    # updates the a parameter of the Testing table
    def updateTestingTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Testing SET TFRecordingID=?, ModelID=? WHERE TestingID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['TFRecordingID'],
            clientAnswer['ModelID'],
            clientAnswer['TestingID']
        ))

        # returns None
        return None
    
    # deletes the defined Testing row
    def deleteTestingTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Testing WHERE TestingID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['TestingID'],))

        return None    
    
    # fetches the Testing from the database
    def fetchTesting(self)-> dict:

        # fetches the Testing from the database
        testing=self.fetchInfo(query='''SELECT * FROM Testing''')

        # returns the Testing
        return testing
    
# class for the table Training
class TrainingTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Training table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertTrainingTable(self, clientAnswer:dict)->int:
        # inserts the Training table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Training (TFRecordingID, ModelID) VALUES (?, ?) ''',
            values=(clientAnswer['TFRecordingID'], clientAnswer['ModelID'])
        )

        # returns the last id of the Training table.
        return lastRowID
    
    # updates the a parameter of the Training table
    def updateTrainingTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Training SET TFRecordingID=?, ModelID=? WHERE TrainingID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['TFRecordingID'],
            clientAnswer['ModelID'],
            clientAnswer['TrainingID']
        ))

        # returns None
        return None
    
    # deletes the defined Training row
    def deleteTrainingTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Training WHERE TrainingID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['TrainingID'],))

        return None  
    
    # fetches the Training from the database
    def fetchTraining(self)-> dict:

        # fetches the Training from the database
        training=self.fetchInfo(query='''SELECT * FROM Training''')

        # returns the Training
        return training
    
# class for the table Model
class ModelTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Model table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertModelTable(self, clientAnswer:dict)->int:
        # inserts the Model table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Model (ModelName, TrainingStatus, CreatedAt, ModelVersionID) VALUES (?, ?, ?, ?) ''',
            values=(clientAnswer.get('ModelName'), clientAnswer.get('TrainingStatus'), clientAnswer.get('CreatedAt'), clientAnswer.get('ModelVersionID'))
        )

        # returns the last id of the Model table.
        return lastRowID
    
    # updates the a parameter of the Model table
    def updateModelTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Model SET ModelName=?, TrainingStatus=?, CreatedAt=?, ModelVersionID=? WHERE ModelID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['ModelName'],
            clientAnswer['TrainingStatus'],
            clientAnswer['CreatedAt'],
            clientAnswer['ModelVersionID'],
            clientAnswer['ModelID']
        ))

        # returns None
        return None
    
    # deletes the defined Model row
    def deleteModelTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Model WHERE ModelID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['ModelID'],))

        return None  
    
    # fetches the Model from the database
    def fetchModel(self)-> dict:

        # fetches the Model from the database
        model=self.fetchInfo(query='''SELECT * FROM Model''')

        # returns the Model
        return model
    
# class for the table ModelVersion
class ModelVersionTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the ModelVersion table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertModelVersionTable(self, clientAnswer:dict)->int:
        # inserts the ModelVersion table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO ModelVersion (ModelVersion, CreatedAt, ModelMetricID, HyperparameterID, ModelWeightsID) VALUES (?, ?, ?, ?, ?) ''',
            values=(clientAnswer.get('ModelVersion'), clientAnswer.get('CreatedAt'), clientAnswer.get('ModelMetricID'), clientAnswer.get('HyperparameterID'), clientAnswer.get('ModelWeightsID'))
        )

        # returns the last id of the ModelVersion table.
        return lastRowID
    
    # updates the a parameter of the ModelVersion table
    def updateModelVersionTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE ModelVersion SET ModelVersion=?, CreatedAt=?, ModelMetricID=?, HyperparameterID=?, ModelWeightsID=? WHERE ModelVersionID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['ModelVersion'],
            clientAnswer['CreatedAt'],
            clientAnswer['ModelMetricID'],
            clientAnswer['HyperparameterID'],
            clientAnswer['ModelWeightsID'],
            clientAnswer['ModelVersionID']
        ))

        # returns None
        return None
    
    # deletes the defined ModelVersion row
    def deleteModelVersionTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM ModelVersion WHERE ModelVersionID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['ModelVersionID'],))

        return None  
    
    # fetches the ModelVersion from the database
    def fetchModelVersion(self)-> dict:

        # fetches the ModelVersion from the database
        modelVersion=self.fetchInfo(query='''SELECT * FROM ModelVersion''')

        # returns the ModelVersion
        return modelVersion

# class for the table ModelMetric
class ModelMetricTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the ModelMetric table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertModelMetricTable(self, clientAnswer:dict)->int:
        # inserts the ModelMetric table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO ModelMetric (MSE, r2, loss) VALUES (?, ?, ?) ''',
            values=(clientAnswer.get('MSE'), clientAnswer.get('r2'), clientAnswer.get('loss'))
        )

        # returns the last id of the ModelMetric table.
        return lastRowID
    
    # updates the a parameter of the ModelMetric table
    def updateModelMetricTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE ModelMetric SET MSE=?, r2=?, loss=? WHERE ModelMetricID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['MSE'],
            clientAnswer['r2'],
            clientAnswer['loss'],
            clientAnswer['ModelMetricID']
        ))

        # returns None
        return None
    
    # deletes the defined ModelMetric row
    def deleteModelMetricTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM ModelMetric WHERE ModelMetricID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['ModelMetricID'],))

        return None  
    
    # fetches the ModelMetric from the database
    def fetchModelMetric(self)-> dict:

        # fetches the ModelMetric from the database
        modelMetric=self.fetchInfo(query='''SELECT * FROM ModelMetric''')

        # returns the ModelMetric
        return modelMetric
    
# class for the table Hyperparameter
class HyperparameterTable(Database):

    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the Hyperparameter table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertHyperparameterTable(self, clientAnswer:dict)->int:
        # inserts the Hyperparameter table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO Hyperparameter (Hyperparameters) VALUES (?) ''',
            values=(clientAnswer.get('Hyperparameters'),)
        )

        # returns the last id of the Hyperparameter table.
        return lastRowID
    
    # updates the a parameter of the Hyperparameter table
    def updateHyperparameterTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE Hyperparameter SET Hyperparameters=? WHERE HyperparameterID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['Hyperparameters'],
            clientAnswer['HyperparameterID']
        ))

        # returns None
        return None
    
    # deletes the defined Hyperparameters row
    def deleteHyperparameterTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM Hyperparameters WHERE HyperparameterID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['HyperparameterID'],))

        return None  
    
    # fetches the Hyperparameter from the database
    def fetchHyperparameter(self)-> dict:

        # fetches the Hyperparameter from the database
        hyperparameter=self.fetchInfo(query='''SELECT * FROM Hyperparameter''')

        # returns the Hyperparameter
        return hyperparameter
    
# class for the table ModelWeights
class ModelWeightsTable(Database):
    
    def __init__(self, dbFile: str)->None:
        super().__init__(dbFile)

    # inserts the ModelWeights table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
    def insertModelWeightsTable(self, clientAnswer:dict)->int:
        # inserts the ModelWeights table. It has to be tested if the inf to be added is already there. If that is the case, no change is needed.
        lastRowID,=self.insertItemsTable(
            query='''INSERT INTO ModelWeights (ModelWeightsPath) VALUES (?) ''',
            values=(clientAnswer.get('ModelWeightsPath'),)
        )

        # returns the last id of the ModelWeights table.
        return lastRowID
    
    # updates the a parameter of the ModelWeights table
    def updateModelWeightsTable(self, clientAnswer:dict)->None:

        # defines the statement of the row update
        statement= "UPDATE ModelWeights SET ModelWeightsPath=? WHERE ModelWeightsID=?"

        # executes the statement
        self.updateItem(updateStatement=statement,Values=(
            clientAnswer['ModelWeightsPath'],
            clientAnswer['ModelWeightsID']
        ))

        # returns None
        return None
    
    # deletes the defined ModelWeights row
    def deleteModelWeightsTable(self, clientAnswer:dict)->None:

        # defines statement to for the deletion of the raw dataset
        statementeSampleTable='DELETE FROM ModelWeights WHERE ModelWeightsID = ?'

        # executes statement
        self.updateItem(updateStatement=statementeSampleTable,Values=(clientAnswer['ModelWeightsID'],))

        return None 
    
    # fetches the ModelWeights from the database
    def fetchModelWeights(self)-> dict:

        # fetches the ModelWeights from the database
        modelWeights=self.fetchInfo(query='''SELECT * FROM ModelWeights''')

        # returns the ModelWeights
        return modelWeights