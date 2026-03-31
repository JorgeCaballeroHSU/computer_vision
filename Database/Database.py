# this files contains the classses for the creation, modification and deletion of the database and its tables

# import required libraries
import sqlite3
from sqlite3 import Error
import datetime

class Database:
    
    # Class' properties
    __filePath:str=''
    
    def __init__(self, dbFile: str)->None:
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        # initialize the connection variable to None
        self.conn = None
        self.__filePath=dbFile

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            self.conn = sqlite3.connect(self.__filePath)
            print(f"Connected to database {self.__filePath} successfully.")

            self.__createTable()
            print("Tables were created successfully.")
        
        # catch any errors that occur during the connection process and print the error message
        except Error as e:
            print(e)

        #return nothing
        return None

    # creates all the tables necessary for running this project. The database table relations can be seen in the document
    # Datenbak - Class Diagram.png
    def __createTable(self)->None:
        """ create a table from the create_table_sql statement
        :return:
        """
        
        # defines the sql-command to create the table named label if this does not exists
        label= "CREATE TABLE IF NOT EXISTS Label (LabelID INTEGER PRIMARY KEY, \
Name TEXT NOT NULL, LabelType TEXT NOT NULL)"

        # defines sthe sql-command for the creation of the table SampleLabel
        sampleLabel="CREATE TABLE IF NOT EXISTS SampleLabel (ID INTEGER PRIMARY KEY, SampleID INTEGER NOT NULL, LabelID INTEGER NOT NULL)"

        # defines the table for the creation of the table Sample
        sample="CREATE TABLE IF NOT EXISTS Sample (SampleID INTEGER PRIMARY KEY, filePath TEXT NOT NULL," \
        "captureTime DATE NOT NULL, isProcessed BOOL NOT NULL, cameraID INTEGER NOT NULL," \
        "DatasetID INTEGER NOT NULL, MaterialID INTEGER NOT NULL, IDTFL: INTEGER NOT NULL)"

        # defines the sql-command for the creation of the table Augmentation
        augmentation=" CREATE TABLE IF NOT EXISTS Augmentation (AugmentationID INTEGER PRIMARY KEY, method TEXT NOT NULL, SampleID INTEGER NOT NULL)"

        # defines the sql-command for the creation of the table CameraInfo
        cameraInfo= "CREATE TABLE IF NOT EXISTS CameraInfo (CameraID INTEGER PRIMARY KEY, manufacturer STRING NOT NULL," \
        "CameraModel TEXT NOT NULL, ISO TEXT NOT NULL, focus TEXT NOT NULL, ExposureTime TEXT NOT NULL, flashMode TEXT NOT NULL,"\
        "focalLength INTEGER NOT NULL, objective TEXT NOT NULL, extension TEXT NOT NULL)"

        # defines the sql-command for the creatiof the table Dataset
        dataset="CREATE TABLE IF NOT EXISTS Dataset (datasetID INTEGER PRIMARY KEY, name TEXT NOT NULL, projectName TEXT NOT NULL,"\
        "created DATE, description TEXT NOT NULL)"

        # defines the sql-command for the creation of the table TFRLabel
        TFRLabel="CREATE TABLE IF NOT EXISTS TFRLabel (IDTFL INTEGER PRIMARY KEY, sampleID INTEGER, IDTFR INTEGER)"

        # defines the sql-command for the creation of the table TFRecording
        TFRecording="CREATE TABLE IF NOT EXISTS TFRecording (IDTFR INTEGER PRIMARY KEY, TFRecording BLOB)"

        # defines the sql-command for the creation of the table MaterialType
        materialType=""

        
        # define the SQL command to create a table named ImageMetadata with various columns 
        # to store metadata about images, including id, label, date, length, width, size, 
        # manufacturer, cameramodel, ISO, focus, exposuretime, flashmode, focallength, 
        # objectiv, extension and preprocessed
        imageMetadata = "CREATE TABLE IF NOT EXISTS ImageMetadata (id INTEGER PRIMARY KEY,\
label TEXT NOT NULL, date DATETIME, length INTEGER, width INTEGER, size INTEGER, \
manufacturer TEXT, cameramodel TEXT, ISO INTEGER, focus TEXT, exposuretime TEXT, \
flashmode TEXT, focallength INTEGER, objectiv TEXT, extension TEXT, preprocessed BOOLEAN,\
auth TEXT, Copyright TEXT, location TEXT, IDTF INTEGER);"

        # define the SQL command to create a table named TFRecording with various columns to 
        # store information about TFRecord files, including IDTF, label and TFRecording (which is a BLOB to store the actual TFRecord data)
        tfRecording = "CREATE TABLE IF NOT EXISTS TFRecording (IDTF INTEGER PRIMARY KEY, label TEXT NOT NULL, TFRecording BLOB);"

        # defines the SQL command to create a table for the models that will be used for the training and evaluation 
        # of the machine learning models, with columns for the model ID, name, training status, mean squared error (MSE), 
        # R-squared (R2) value, hyperparameters and model weights (stored as a BLOB)
        modelTable = "CREATE TABLE IF NOT EXISTS ModelTable (modelID INTEGER PRIMARY KEY, modelname TEXT NOT NULL, \
trainingStatus TEXT, MSE FLOAT, R2 FLOAT, hyperparameters TEXT, modelweight BLOB);"

        # execute the SQL commands to create the tables in the database, and print a success message if the tables are created successfully. If any errors occur during the execution of the SQL commands, catch the error and print the error message.
        try:
            c = self.conn.cursor()
            c.execute(imageMetadata)
            c.execute(tfRecording)
            c.execute(modelTable)

            # commit the changes to the database to ensure that the tables are created and any changes are saved
            self.conn.commit()

            # print a success message to indicate that the tables were created successfully
            print("Table created successfully.")
        
        # catch any errors that occur during the execution of the SQL commands and print the error message
        except Error as e:

            # if an error occurs, print the error message to help diagnose the issue
            print(e)

        # return nothing
        return None

    # module to add a new item to table ImageMetadata
    def addItemImagMeta(self,label:str, date:datetime.datetime, length:int, width:int, size:int,
                        manuf:str, cameraMode:str, ISO:str, focus:str, exposureTime: str,
                        flashMode:str, focalLength:int, objective: str, extension:str, preprocessed:bool,
                        author:str, copyright:str, location:str, IDTF:int, tableName:str='ImageMetadata')->None:

        # insert table statement
        insertStatement='''INSERT INTO {}({},{},{},{},{},{},{},{},{},\
{},{},{},{},{},{},{},{},{},{})'''.format(tableName, label,date,length,width,size,manuf,cameraMode,ISO,focus,
                                         exposureTime,flashMode,focalLength,objective,extension,preprocessed,author,
                                         copyright,location,IDTF)

        # executes the statement
        self.conn.execute(insertStatement)

        # commits statement
        self.conn.commit()

        # closes connection
        self.__closeConnection()

        # return None
        return None
    
    # module to add a new item to table TFRecording
    def addItemTFRecording(self,label:str, TFRecoding: bytearray,tableName:str='TFRecording')->None:

        # opens connection to the db
        self.__openConnection()

        # insert table statement
        insertStatement='''INSERT INTO {}({}, {})'''.format(tableName,label,TFRecoding)

        # executes statemtent
        self.conn.execute(insertStatement)

        #commits to statement
        self.conn.commit()

        #closes connection
        self.__closeConnection

        #returns None
        return None
    
    # module to add a new item to table ModelTable
    def addItemModelTable(self,modelName:str,trainingStatus:str,MSE:float,r2:float,hyperparameters:str, modelWeights:bytearray,
                          tableName:str='ModelTable')-> None:

        # opens connection to the db
        self.__openConnection()

        # insert table statement
        insertStatement='''INSERT INTO {}({}, {}, {}, {}, {}, {})'''.format(tableName,modelName,trainingStatus,MSE,r2,hyperparameters,modelWeights)

        # executes statement
        self.conn.execute(insertStatement)

        # commits to statement
        self.conn.commit()

        #closes connection
        self.__closeConnection

        # returns nothing
        return None

    # module to fetch information from the database
    def fetchInfo(self,statement:str)-> tuple:

        # opens connection to the db
        self.__openConnection()

        # fetches the elements indicated by the statement
        fetchedElement=self.conn.cursor().execute(statement).fetchall()

        #closes connection
        self.__closeConnection

        # returns nothing
        return  fetchedElement


    # module to update an existing element
    def updateItem(self, updateStatement:str, Values:tuple)->None:

        # opens connection to the db
        self.__openConnection()

        # executes the given statement
        self.conn.cursor().execute(updateStatement,Values)

        # commits executed statement
        self.conn.commit()

        #closes connection
        self.__closeConnection

        # returns nothing
        return None

    # module to open connection to the database
    def __openConnection(self)->None:

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            self.conn = sqlite3.connect(self.__filePath)
            print(f"Connected to database {self.__filePath} successfully.")
        
        # catch any errors that occur during the connection process and print the error message
        except Error as e:
            print(e)

        # returns none
        return None

    # module to close connections to the database
    def __closeConnection(self)->None:
        """ close the database connection
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

        # return nothing
        return None