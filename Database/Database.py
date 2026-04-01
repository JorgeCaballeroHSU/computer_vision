# this files contains the classses for the creation, modification and deletion of the database and its tables

# import required libraries
import sqlite3
from sqlite3 import Error

class Database:
    
    # Class' properties
    __filePath:str=''
    
    def __init__(self, dbFile: str)->None:
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        # initialize the connection variable to None
        self.__filePath=dbFile

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            
            self.__createTable()
        
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
        label= "CREATE TABLE IF NOT EXISTS Label (LabelID INTEGER PRIMARY KEY," \
        "Name TEXT NOT NULL, LabelType TEXT NOT NULL);"

        # defines sthe sql-command for the creation of the table SampleLabel
        sampleLabel="CREATE TABLE IF NOT EXISTS SampleLabel (ID INTEGER PRIMARY KEY, " \
        "SampleID INTEGER NOT NULL, " \
        "LabelID INTEGER NOT NULL," \
        "FOREIGN KEY(SampleID) REFERENCES Sample(SampleID)," \
        "FOREIGN KEY(LabelID) REFERENCES Label(LabelID));"

        # defines the table for the creation of the table Sample
        sample="CREATE TABLE IF NOT EXISTS Sample (SampleID INTEGER PRIMARY KEY, filePath TEXT NOT NULL," \
        "captureTime DATE NOT NULL, isProcessed INTEGER NOT NULL, cameraID INTEGER NOT NULL," \
        "DatasetID INTEGER NOT NULL, MaterialID INTEGER NOT NULL, IDTFL INTEGER NOT NULL," \
        "AugmentationID INTEGER," \
        "FOREIGN KEY(cameraID) REFERENCES CameraInfo(CameraID)," \
        "FOREIGN KEY(DatasetID) REFERENCES Dataset(datasetID)," \
        "FOREIGN KEY(MaterialID) REFERENCES MaterialType(IDMT) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(IDTFL) REFERENCES TRFLabel(IDTFL)," \
        "FOREIGN KEY (AugmentationID) REFERENCES Augmentation(AugmentationID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table Augmentation
        augmentation=" CREATE TABLE IF NOT EXISTS Augmentation (AugmentationID INTEGER PRIMARY KEY, method TEXT NOT NULL, " \
        "SampleID INTEGER NOT NULL," \
        "FOREIGN KEY(SampleID) REFERENCES Sample(SampleID));"

        # defines the sql-command for the creation of the table CameraInfo
        cameraInfo= "CREATE TABLE IF NOT EXISTS CameraInfo (CameraID INTEGER PRIMARY KEY, manufacturer TEXT NOT NULL," \
        "CameraModel TEXT NOT NULL, ISO TEXT NOT NULL, focus TEXT NOT NULL, ExposureTime TEXT NOT NULL, flashMode TEXT NOT NULL,"\
        "focalLength INTEGER NOT NULL, objective TEXT NOT NULL, extension TEXT NOT NULL);"

        # defines the sql-command for the creation of the table Dataset
        dataset="CREATE TABLE IF NOT EXISTS Dataset (datasetID INTEGER PRIMARY KEY, name TEXT NOT NULL, projectName TEXT NOT NULL,"\
        "created DATE, description TEXT NOT NULL);"

        # defines the sql-command for the creation of the table TFRLabel
        TFRLabel="CREATE TABLE IF NOT EXISTS TFRLabel (IDTFL INTEGER PRIMARY KEY, sampleID INTEGER, IDTFR INTEGER," \
        "FOREIGN KEY(sampleID) REFERENCES Sample(SampleID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY(IDTFR) REFERENCES TFRecording(IDTFR) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table TFRecording
        TFRecording="CREATE TABLE IF NOT EXISTS TFRecording (IDTFR INTEGER PRIMARY KEY, TFRecording BLOB, IDTFL INTEGER," \
        "FOREIGN KEY(IDTFL) REFERENCES TFRLabel(IDTFL) ON DELETE CASCADE ON UPDATE CASCADE);"

        # defines the sql-command for the creation of the table MaterialType
        materialType="CREATE TABLE IF NOT EXISTS MaterialType (IDMT INTEGER PRIMARY KEY, mm0063 REAL, " \
        "mm0125 REAL, mm0400 REAL, mm0500 REAL, mm1000 REAL, mm2000 REAL, mm4000 REAL," \
        "mm8000 REAL, mm1600 REAL, mm3200 REAL, SampleID INTEGER);"

        # defines the sql-command for the creation of the table ModelMetric
        modelMetric="CREATE TABLE IF NOT EXISTS modelMetric (MetricID INTEGER PRIMARY KEY, MSE REAL, r2 REAL, " \
        "loss REAL);"

        # defines the sql-command for the creation of the table Hyperparameter
        Hyperparameter= "CREATE TABLE IF NOT EXISTS Hyperparameter (HPID INTEGER PRIMARY KEY, hyperparameter TEXT);"

        # defines the sql-command for the creation of the table ModelWeights
        modelWeights= "CREATE TABLE IF NOT EXISTS ModelWeights(MWID INTEGER PRIMARY KEY, modelWeights BLOB);"

        # defines the sql-command for the creation of the table Model
        model= "CREATE TABLE IF NOT EXISTS Model (ModelID INTEGER PRIMARY KEY, modelName TEXT, architecture TEXT, " \
        "trainingStatus TEXT, createdAt DATE, MetricID INTEGER, HPID INTEGER, Weights INTEGER," \
        "FOREIGN KEY (MetricID) REFERENCES modelMetric(MetricID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY (HPID) REFERENCES Hyperparameter(HPID) ON DELETE CASCADE ON UPDATE CASCADE," \
        "FOREIGN KEY (Weights) REFERENCES ModelWeights(MWID) ON DELETE CASCADE ON UPDATE CASCADE);"

        # gets all the variables in one place to execute them
        tables = [
            label, sampleLabel, sample, augmentation, cameraInfo,
            dataset, TFRLabel, TFRecording, materialType,
            modelMetric, Hyperparameter, modelWeights, model]

        # execute the SQL commands to create the tables in the database, and print a success message if the tables are created successfully. If any errors occur during the execution of the SQL commands, catch the error and print the error message.
        try:
            
            # opens connection
            self.__openConnection()

            # calls the cursor function
            c = self.conn.cursor()

            # loops throught the variables to execute the sql-commands
            for table in tables:
                  
                # executes the commands to create the tables
                c.execute(table)

            # commit the changes to the database to ensure that the tables are created and any changes are saved
            self.conn.commit()
        
        # catch any errors that occur during the execution of the SQL commands and print the error message
        except Error as e:

            # if an error occurs, print the error message to help diagnose the issue
            print(e)

            # rolls back
            self.conn.rollback()

        # closes the connection at the end of the session+
        finally:

            # closes connection
            self.__closeConnection()

        # return nothing
        return None

    # inserts new items in a table
    def insertItemsTable(self, query: str, values: tuple = ()) -> tuple:
        """ Safely insert data into a table using parameterized queries.

        :param query: SQL INSERT statement with placeholders (?)
        :param values: tuple of values to insert """ 

        try:
            # open connection
            self.__openConnection()

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

        finally:

            # always close connection
            self.__closeConnection()
    
    # module to fetch information from the database
    def fetchInfo(self,statement:str)-> tuple:

        # initializes the variable
        fetchedElement=()

        # opens a try block to cath errors
        try:
            # opens connection to the db
            self.__openConnection()

            # fetches the elements indicated by the statement
            fetchedElement=self.conn.cursor().execute(statement).fetchall()
            
            # returns fetched elements
            return  fetchedElement

        # catches errors during execution
        except Error as e:

            # prints the error found
            print(f'Error fetching data: {e}')

            # returns empty tuple
            return ()
        
        # closes the connection after everything is done
        finally:
            
            #closes connection
            self.__closeConnection()

        

    # module to update an existing element
    def updateItem(self, updateStatement:str, Values:tuple)->tuple:

        # opens try block to catch errors
        try:

            # opens connection to the db
            self.__openConnection()

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

        # closes the connection when everything is done
        finally:

            #closes connection
            self.__closeConnection()

    # module to open connection to the database
    def __openConnection(self)->None:

        # attempt to connect to the database using the provided file name and print a success message if the connection is successful
        try:
            self.conn = sqlite3.connect(self.__filePath)
            self.conn.execute("PRAGMA foreign_keys = ON;")

        # catches any errors that occur during the connection process and print the error message
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

        # return nothing
        return None