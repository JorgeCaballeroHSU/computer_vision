# this files contains the classses for the creation, modification and deletion of the database and its tables

# import required libraries
import sqlite3
from sqlite3 import Error
import datetime

class Database:
    
    
    def __init__(self, dbFile: str)->None:
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """

        # initialize the connection variable to None
        self.conn = None

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            self.conn = sqlite3.connect(dbFile)
            print(f"Connected to database {dbFile} successfully.")
        
        # catch any errors that occur during the connection process and print the error message
        except Error as e:
            print(e)

        #return nothing
        return None

    def createTable(self)->None:
        """ create a table from the create_table_sql statement
        :return:
        """
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

        # return None
        return None
    
    # module to add a new item to table TFRecording
    def addItemTFRecording(self,label:str, TFRecoding: bytearray,tableName:str='TFRecording')->None:

        # insert table statement
        insertStatement='''INSERT INTO {}({}, {})'''.format(tableName,label,TFRecoding)

        # executes statemtent
        self.conn.execute(insertStatement)

        #commits to statement
        self.conn.commit()

        #returns None
        return None
    
    # module to add a new item to table ModelTable
    def addItemModelTable(self,modelName:str,trainingStatus:str,MSE:float,r2:float,hyperparameters:str, modelWeights:bytearray,
                          tableName:str='ModelTable')-> None:

        # insert table statement
        insertStatement='''INSERT INTO {}({}, {}, {}, {}, {}, {})'''.format(tableName,modelName,trainingStatus,MSE,r2,hyperparameters,modelWeights)

        # executes statement
        self.conn.execute(insertStatement)

        # commits to statement
        self.conn.commit()
        
        # returns nothing
        return None

    def close_connection(self)->None:
        """ close the database connection
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

        # return nothing
        return None