#imports required libraries
from importlib.resources import path

from Sockets.SocketServer import SocketServer
from Tools.ChangePath import ChangePath
from Tools.Format import addDataType
from Files.Path import Path
from Files.Label import Label
from Database.Database import *
from Preprocessing.TFRecorder import TFRecorder
import os
from PIL import Image
from PIL.ExifTags import TAGS

# windows-formatted address to store the pictures
windowsAddress=r'C:\Users\Admin\OneDrive - Helmut-Schmidt-Universität\Dokumente\Computer Vision Project\01 Pictures'

# object to change the path formatting from windows to linux and viseversa
pathFormat=ChangePath()

# changes in the dataset table. Returns bool indicating if the process was a success (True) or something failed (False)
def Dataset(clientDataset:dict|None, table:DatasetTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertDatasetTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updateDatasetTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deleteDatasetTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchDataset()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
# does all necessary changes to CameraInfo table and returns bool indicating whether the changes were successfull and as well the last row 
def CameraInfo(clientDataset:dict|None, table:CameraInfoTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertCameraInfoTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchCameraInfo()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchCameraInfo()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updateCameraInfoTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchCameraInfo()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.updateCameraInfoTable()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deleteCameraInfoTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchCameraInfo()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchCameraInfo()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
# does all necessary changes to MaterialType table and returns bool indicating whether the changes were successfull and as well the last row 
def MaterialType(clientDataset:dict|None, table:MaterialTypeTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertMaterialTypeTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updateMaterialTypeTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deleteMaterialTypeTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchMaterialType()

            # as there was an error, returns False
            return [False, actualDatabase,None]

# does all necessary changes to Sample table and returns bool indicating whether the changes were successfull and as well the last row 
def Sample(clientDataset:dict|None, table:SampleTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertSampleTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updateSampleTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deleteSampleTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchSample()

            # as there was an error, returns False
            return [False, actualDatabase,None]


# does all necessary changes to JunctionPre table and returns bool indicating whether the changes were successfull and as well the last row 
def JunctionPre(clientDataset:dict|None, table:JunctionPreTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertJunctionPreTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updateJunctionPreTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deleteJunctionPreTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchJunctionPre()

            # as there was an error, returns False
            return [False, actualDatabase,None]


# does all necessary changes to Preprocessing table and returns bool indicating whether the changes were successfull and as well the last row 
def Preprocessing(clientDataset:dict|None, table:PreprocessingTable, action: str='add')->list[bool, dict,int |None]:

    '''Handles the acces of the Table Dataset according to the requirements of the client. \n
    :param clientDataset: Dictionary with information required to add or modifiy new projects.
    :param table: Database table handler.
    :param action: Type of action to be made. There are only three options 'add', 'modify', and 'delete' to add, modify, and delete the database.
    :return: bool indicating if the process was a success.
    '''

    # executes code according to the action
    if action=='add':

        try:
            # adds new project to the database
            lastIdRow=table.insertPreprocessingTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            return [True,actualDatabase,lastIdRow]
        
        #in case of error return false
        except Exception as e:
            
            # prints the error
            print('An error has occured. Error:{}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    # if the actions is to modify an existing project of the dataset table
    elif action=='modify':

        try:

            # modify the indicated row of the table
            table.updatePreprocessingTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            # as there was an error, returns False
            return [False, actualDatabase,None]
        
    elif action=='delete':

        try: 

            # deletes the indicated row
            table.deletePreprocessingTable(clientAnswer=clientDataset)

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            # returns results
            return[True, actualDatabase, None]
        
        except Exception as e:

            # prints error
            print('An error has occured. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase=table.fetchPreprocessing()

            # as there was an error, returns False
            return [False, actualDatabase,None]


# handles all necessary changes to JunctionAugmentation table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def JunctionAugmentation(clientData: dict | None, table: JunctionAugmentationTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the JunctionAugmentation table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertJunctionAugmentationTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateJunctionAugmentationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteJunctionAugmentationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchJunctionAugmentation()

            # returns results
            return [False, actualDatabase, None]

# handles all necessary changes to Augmentation table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Augmentation(clientData: dict | None, table: AugmentationTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Augmentation table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertAugmentationTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateAugmentationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteAugmentationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchAugmentation()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to TFRecording table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def TFRecording(clientData: dict | None, table:TFRecordingTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the TFRecording table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertTFRecordingTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchTFRecording()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTFRecording()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateTFRecordingTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchTFRecording()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTFRecording()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteAugmentationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchAugmentation()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchAugmentation()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to Validation table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Validation(clientData: dict | None, table:ValidationTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Validation table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertValidationTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchValidation()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchValidation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateValidationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchValidation()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchValidation()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteValidationTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchValidation()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchValidation()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to Testing table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Testing(clientData: dict | None, table:TestingTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Testing table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertTestingTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchTesting()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTesting()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateTestingTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchTesting()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTesting()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteTestingTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchTesting()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchTesting()

            # returns results
            return [False, actualDatabase, None]

# handles all necessary changes to Training table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Training(clientData: dict | None, table:TrainingTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Training table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertTrainingTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchTraining()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTraining()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateTrainingTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchTraining()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchTraining()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteTrainingTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchTraining()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchTraining()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to Model table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Model(clientData: dict | None, table:ModelTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Model table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertModelTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchModel()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModel()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateModelTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModel()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModel()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteModelTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModel()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchModel()

            # returns results
            return [False, actualDatabase, None]

# handles all necessary changes to ModelVersion table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def ModelVersion(clientData: dict | None, table:ModelVersionTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the ModelVersion table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertModelVersionTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchModelVersion()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelVersion()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateModelVersionTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelVersion()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelVersion()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteModelVersionTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelVersion()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchModelVersion()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to ModelMetric table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def ModelMetric(clientData: dict | None, table:ModelMetricTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the ModelMetric table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertModelMetricTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchModelMetric()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelMetric()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateModelMetricTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelMetric()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelMetric()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteModelMetricTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelMetric()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchModelMetric()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to Hyperparameter table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def Hyperparameter(clientData: dict | None, table:HyperparameterTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the Hyperparameter table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertHyperparameterTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchHyperparameter()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchHyperparameter()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateHyperparameterTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchHyperparameter()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchHyperparameter()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteHyperparameterTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchHyperparameter()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchHyperparameter()

            # returns results
            return [False, actualDatabase, None]
        
# handles all necessary changes to ModelWeights table and returns:
# [success flag, actual database state, last inserted row id (if any)]
def ModelWeights(clientData: dict | None, table:ModelWeightsTable, action: str = 'add') -> list[bool, dict, int | None]:

    '''
    Handles access to the ModelWeights table according to client requirements.

    :param clientData: Dictionary with information required to add/modify/delete entries.
    :param table: Database table handler.
    :param action: Type of action ('add', 'modify', 'delete').
    :return: [bool success, dict database snapshot, int | None lastRowID]
    '''

    # ADD
    if action == 'add':
        try:
            # adds new project to the database
            lastIdRow = table.insertModelWeightsTable(clientAnswer=clientData)

            # gets the actual composition of the database
            actualDatabase = table.fetchModelWeights()

            # returns results
            return [True, actualDatabase, lastIdRow]

        # in case of error return false
        except Exception as e:
            
            # prints error
            print('An error has occurred. Error: {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelWeights()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # MODIFY
    elif action == 'modify':
        try:
            # modify the indicated row of the table
            table.updateModelWeightsTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelWeights()

            # as there was an error, returns False
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual composition of the database
            actualDatabase = table.fetchModelWeights()

            # as there was an error, returns False
            return [False, actualDatabase, None]

    # DELETE
    elif action == 'delete':

        try:

            # deletes the indicated row
            table.deleteModelWeightsTable(
                clientAnswer=clientData
            )

            # gets the actual composition of the database
            actualDatabase = table.fetchModelWeights()

            # returns results
            return [True, actualDatabase, None]

        except Exception as e:

            # prints error
            print('An error has occurred. Error {}'.format(e))

            # gets the actual compostion of the database
            actualDatabase = table.fetchModelWeights()

            # returns results
            return [False, actualDatabase, None]


# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(socketServer:SocketServer, label:Label,path:Path, database:Database)->dict:
    
    # gets the image from the client
    # It assumes that the client will send the image as chucks that will be put together at the socket class
    # it assumes that the picture will be received as binary that will be decoded at the socket class
    # it assumes that the pciture will be received as a part of a dictionary with some other metadata.
    # this medatadata will be used to fill up the database
    clientAnswer:dict=socketServer.receive() # it assumes that the chucks of the image will be 
    # addended together in the socker class and that the chunks of the image will be added together

    # stores the image in the defined path
    # sets the path to save the files
    path.setPath(path=pathFormat.changePathWindowsToWsl(path=windowsAddress))

    # generates label for the picture
    label.setLabelType(labelType=clientAnswer.get('labelType')) # sets the label type
    labelFile=label.generateSampleLabel()

    # creates a file where the image is going to be saved
    with open(
        file=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')),
        mode='wb'
        ) as f:

        # saves the file
        f.write(clientAnswer.pop('image')) #-> client answer contains the image as binary

        # closes the file when is over
        f.close()


# defines the function databaseFill to fill up date database of images for later training
def dataBaseFill(socketServer:SocketServer, label:Label,path:Path, database:Database)->dict:
    
    # gets the image from the client
    # It assumes that the client will send the image as chucks that will be put together at the socket class
    # it assumes that the picture will be received as binary that will be decoded at the socket class
    # it assumes that the pciture will be received as a part of a dictionary with some other metadata.
    # this medatadata will be used to fill up the database
    clientAnswer:dict=socketServer.receive() # it assumes that the chucks of the image will be 
    # addended together in the socker class and that the chunks of the image will be added together

    # stores the image in the defined path
    # sets the path to save the files
    path.setPath(path=pathFormat.changePathWindowsToWsl(path=windowsAddress))

    # generates label for the picture
    label.setLabelType(labelType=clientAnswer.get('labelType')) # sets the label type
    labelFile=label.generateSampleLabel()

    # creates a file where the image is going to be saved
    with open(
        file=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg')),
        mode='wb'
        ) as f:

        # saves the file
        f.write(clientAnswer.pop('image')) #-> client answer contains the image as binary

        # closes the file when is over
        f.close()



# gets the pcitures into a TensorFlow record format for later use in the training of the model
def generateTensorFlowRecords(path:Path, database:Database, tfRecorder:TFRecorder, labelFile:str)->None:

    #creates a TensorFlow record

    # gets the file path of the file
    filePath=''.join(path.getPath(),addDataType(fileName=labelFile,dataType='jpeg'))

    # creates the TF record with the file path, the label and the labelInit
    record=tfRecorder.createTFRecord(
        fileName=filePath,
        label=labelFile,
        labelInit=database.fetchInfo(query='''SELECT LabelID FROM label WHERE name=?''', values=(labelFile, 
        ))[0]['LabelID'])
    
    # saves the TF record in the indicated location
    tfRecorder.saveTFRecord(
        fileName=''.join(labelFile,'tfrec'),
        filePath=path.getPath(),
        TFRecord=record
    )

    # updates the table TFrecording the binary of the TF record.
    database.insertItemsTable(
        query='''INSERT INTO TFRecording (name, label, labelInit, filePath) VALUES (?, ?, ?, ?) ''',
        values=(labelFile, labelFile, database.fetchInfo(query='''SELECT LabelID FROM label WHERE name=?''', values=(labelFile, 
        ))[0]['LabelID'], ''.join(path.getPath(),addDataType(fileName=labelFile,dataType='tfrec')))
    )





# imports more required libraries
from Preprocessing.DataAugmentation import Flipping, ColorDistortion

# transforms the images
def transformImages(path:Path,flip:Flipping, colDis:ColorDistortion,datenBank:Database,timesPerFoto:int=10)->None:

    # gets the path where the images are located
    fotosPath=path.getPath()

    # gets a list of files avialables in the path
    filesAvailable=os.listdir(path=fotosPath)

    #loops through every file available
    for file in filesAvailable:
        
        # generates the address of the file and opens it for use read only.
        photoLocation= open('/'.join(fotosPath,file),mode='r')

        # in this loop the transformations will be done
        for i in range(0, timesPerFoto):

            # flips the image two times randomly
            if i==0 or i==1:
                
                # flips randomly the image
                file=flip.flip(image=photoLocation)

            # distors randomly the image several times.
            # provides timesPerFoto-2 of these random distorsions
            else:

                # distors the image
                file=colDis.distortColors(image=photoLocation)

        # closes the file
        photoLocation.close()

        datenBank.addItemTFRecording(label='', TFRecoding=file)
        

    # returns None
    return None
