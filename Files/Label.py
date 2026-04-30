# # This python code is in charge of the labelling of the fotographs according to the conventions of the project. 
# It is used to label the files that reside in a separated folder

# import the necessary libraries
from Database.Database import DatasetTable, PreprocessingTable, JunctionPreTable, SampleTable

# # creates class for the labelling of the photographs
class LabelSample(DatasetTable):

    '''This class is in charge of the labelling of the photographs according to the conventions of the project. It is used to label the photographs with the name of the person and the date of the photograph.'''

    # properties of the class
    _projectName:str='' # that is the label name or the project name
    _materialType:str='' # type of material. It can be S(sand), K (kies), T (ton), M (gemischt)
    _dataSetID:int=0 # dataset ID, that is the ID of the Dataset table
    _sampleNumber:int=0 # last sample number in the database
    

    # methods of the class
    def __init__(self, dbFile:str) ->None:
        '''This method is the constructor of the class. It initializes the properties of the class.'''

        # calls the constructor of the parent class
        super().__init__(dbFile=dbFile)
        
    
    # sets the properties _projectName and _materialType
    def setProperties(self) ->bool:

        # calls the function to fetch the material type from the database
        materialType=self.fetchDataset()

        # Checks if the material type is empty.
        if bool(materialType):
            
            # sets the material type parameter
            self._materialType=materialType[0]['MaterialType'] # sets the material type

            # sets the project name parameter
            self._projectName=materialType[0]['ProjectName'] # sets the project name

            # sets the dataset ID parameter
            self._dataSetID=materialType[0]['DatasetID'] # sets the dataset ID
            
            # returns True to indicate that the label type was set successfully
            return True
        
        # if the material type is empty, returns False to indicate that the label type was not set successfully
        else:

            self._materialType='' # sets the material type to empty string
            self._projectName='' # sets the project name to empty string

            # Returns False to indicate that te label properties were not set.
            return False
    
    # gets the sample number
    def __getSampleNumber(self) ->int:
        
        '''This method gets the sample number. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # creates a new statement to download the sample ID
        statement="SELECT DatasetID FROM Sample WHERE DatasetID={}".format(self._dataSetID)

        # downloads the values according to the statement
        sampleLabelTable=self.fetchInfo(statement=statement)

        # checks if the list is empty
        if not sampleLabelTable:

            # if the list is empty returns 0, indicating no available information
            return 0
        
        # if the table is not empty, fills up the required variables
        else:

            # returns the number of samples in the database, related to the DatasetID
            return len(sampleLabelTable)
        
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
        label ='_'.join( [self._projectName , self._materialType , str(self._sampleNumber).zfill(3)])

        # expected output example: "ProjectName_MaterialType_SampleNumber", HSU-HH_K_001 where SampleNumber is a three digit number with leading zeros if necessary.

        # returns the label for the photograph
        return label
    

# class for the generation of the labels for the preprocessed files
class LabelPreprocessing ():

    ''' This class is in charge of the label generation for the preprocessing files.'''

    def __init__(self, sampleLabel:str,preprocessingType:str='None') ->None:
        '''This method is the constructor of the class. It initializes the properties of the class.'''

        # defines content of the properties
        self._sampleLabel=sampleLabel
        self._preprocessingType=preprocessingType

    # sets the value of the properties
    def setProperties(self, sampleLabel:str,preprocessingType:str=None)->None:

        # defines content of the properties
        self._sampleLabel=sampleLabel
        self._preprocessingType=preprocessingType

    # generates label for preprocessing files
    def generatePreprocessingLabel(self)->str:

        # generates the label. Label example -> HSU-HH_S_001_F -> Project: HSU-HH. Sample type: S= Sand. 001 Sample one. Type of preprocessing: F=Flipping
        label='_'.join([self._sampleLabel,self._preprocessingType])

        # returns generated label as string
        return label
        

# creates labels for the TFRecording files
class LabelTFRecording():
    ''''''
    
    # spaces for properties of the class

    def __init__(self, preprocessingLabel:str, augmentationType:str)->None:

        # defines content of the class properties
        self._preprocessingLabel= preprocessingLabel
        self._augmentationType= augmentationType

        # returns None
        return None
    
    # sets properties 
    def setProperties(self, preprocessingLabel:str, augmentationType:str)->None:

        # defines content of the class properties
        self._preprocessingLabel= preprocessingLabel
        self._augmentationType= augmentationType

        # returns None
        return None
    # generates the label for the TensorFlow Record
    def generateTensorFlowRecordLabel(self)->str:

        # joins the strings to generate the label
        label='_'.join([self._preprocessingLabel,self._augmentationType])

        # returns label
        return label

        
