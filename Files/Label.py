# # This python code is in charge of the labelling of the fotographs according to the conventions of the project. 
# It is used to label the files that reside in a separated folder

# import the necessary libraries
import re # regular expression library to check for the label convertions of the project
from Database.Database import Database

# # creates class for the labelling of the photographs
class Label:

    '''This class is in charge of the labelling of the photographs according to the conventions of the project. It is used to label the photographs with the name of the person and the date of the photograph.'''

    # properties of the class
    _name:str='HSU_HH_CVP_' # that is the label name or the project name
    _labelType:str='' # type of material. It can be S(sand), K (kies), T (ton), M (gemischt)
    _sampleNumber:int=0 # last sample number in the database
    

    # methods of the class
    def __init__(self) ->None:
       self._labelDatabase=Database(dbFile='ComputerVision.db')
        
    
    # sets the label type
    def setLabelType(self, labelType:str) ->bool:

        # checks if the labelType provided is according the label conventions of the project
        if labelType not in ['S', 'K', 'T', 'M']:
            
            # if the labelType provided is not according the label conventions of the project, then informs about it and returns False
            print('The label type {} is not valid. Please check the label type and try again.'.format(labelType))

            # returns False to indicate that the label type is not valid
            return False
        
        # if labelType is provided according the label convetions, then set the variable _labelType with the value of labelType
        else:

            # sets the variable
            self._labelType=labelType

            # if everything went smoothly, then indicate return True.
            return True
        
    
    # gets the sample number
    def __getSampleNumber(self) ->int:
        
        '''This method gets the sample number. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # creates a new statement to download the sample ID
        statement="SELECT * FROM SampleLabel ORDER BY SampleID DESC LIMIT 1"

        # downloads the properties for the variable _sampleNumber
        sampleLabelTable=self._labelDatabase.fetchInfo(statement=statement)

        # checks if the table is empty
        if not sampleLabelTable:

            # if the table is empty returns 0, indicating no available information
            return 0
        
        # if the table is not empty, fills up the required variables
        else:

            # returns the sample number
            return int(sampleLabelTable[0]['SampleID'])
        
    # sets sampleNumber
    def __setSampleNumber(self) ->bool:
        '''This method sets the sample number. It is used to label the photographs with the name of the person and the date of the photograph.'''
        
        # gets the actual latest sample number in the database
        dbSampleNumber=self.__getSampleNumber()

        # sets the sample number
        self._sampleNumber=dbSampleNumber+1

        # returns True to indicate that the sample number was set successfully
        return True

    # generates the label for the photograph.
    def generateSampleLabel(self) ->str:
        
        '''This method generates the label for the photograph. It is used to label the photographs with the name of the person and the date of the photograph.'''
        
        # sets the sample number
        self.__setSampleNumber()

        # generates the label for the photograph
        label ='_'.join( [self._name , self._labelType , str(self._sampleNumber).zfill(3)])

        # returns the label for the photograph
        return label
