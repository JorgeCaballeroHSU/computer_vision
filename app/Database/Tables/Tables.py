# imports required variables
from app.Database.Database import *

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

