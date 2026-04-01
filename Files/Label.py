# This python code is in charge of the labelling of the fotographs according to the conventions of the project. It is used to label the photographs with the name of the person and the date of the photograph.

# imports the necessary libraries
from Database.Database import Database

# creates class for the labelling of the photographs
class Label:

    '''This class is in charge of the labelling of the photographs according to the conventions of the project. It is used to label the photographs with the name of the person and the date of the photograph.'''

    # properties of the class
    __projectName: str = ""
    __sampleNumber: str = ""
    __typeMaterial: str = ""
    __AugmentedNumber:str = ""
    __labelDatabase=Database(dbFile='ComputerVision.db'
                           )

    # methods of the class
    def __init__(self) ->None:
       
       # checks if the properties of the class are empty
        if self.__projectName == "" or self.__sampleNumber == "" or self.__typeMaterial == "":
            
            # if the properties of the class are empty, tries to download the properties of the class from the database
            boolValue = self.downloadProperties()

            #if self.downloadProperties() == False, then the properties are still empty
            if boolValue == False:
                pass
            else:
                # if the properties of the class are not empty, then the properties of the class are downloaded from the database
                pass

    # downloads properties of the class from the database
    def downloadProperties(self, labelType:str='Sand') ->bool:

        '''This method downloads the properties of the class from the database. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # labelType can be Sand, Gravel, Silt, Mix.

        # creates the statement to fetch the available information
        statement="SELECT * FROM Label WHERE labelType ={}".format(labelType)

        # downloads the properties of the class from the database
        labelTable=self.__labelDatabase.fetchInfo(statement=statement)

        # checks if the table is empty
        if not all(labelTable):
            
            # if the table is empty returns False, indicating no information
            return False

        # if the table is not emply, fills up the required variables
        else:

            # sets up the variable __projectName
            self.__projectName=labelTable[1].split('_')[0]

            # sets up the variable __typeMaterial
            self.__typeMaterial=labelTable[1].split('_')[1]

            # sets up the variable __sampleNumber



            # returns True if the table contains information that can be used to fill up the variables
            return True
        

    # uploads properties of the class to the database
    def uploadProperties(self) ->None:

        '''This method uploads the properties of the class to the database. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # uploads the properties of the class to the database
        # code to upload the properties of the class to the database goes here

        # returns nothing
        return None
    

    # sets the project name
    def setProjectName(self, projectName: str) ->None:

        '''This method sets the project name. It is used to label the photographs with the name of the person and the date of the photograph.'''
        
        # sets the project name
        self.__projectName = projectName

        # returns nothing
        return None

    # gets the project name
    def getProjectName(self) ->str:

        '''This method gets the project name. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # returns the project name
        return self.__projectName

    # sets the sample number
    def setSampleNumber(self, sampleNumber: str) ->None:

        '''This method sets the sample number. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # sets the sample number
        self.__sampleNumber = sampleNumber

        # returns nothing
        return None

    # gets the sample number
    def getSampleNumber(self) ->str:

        '''This method gets the sample number. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # returns the sample number
        return self.__sampleNumber

    # gets the type of material
    def getTypeOfMaterial(self) ->str:

        '''This method gets the type of material. It is used to label the photographs with the name of the person and the date of the photograph.'''
    
        # returns the type of material
        return self.__typeMaterial

    # sets the type of material
    def setTypeOfMaterial(self,typeMaterial: str) ->str:

        '''This method sets the type of material. It is used to label the photographs with the name of the person and the date of the photograph.'''
        self.__typeMaterial = typeMaterial

        # returns nothing
        return None

    # generates the label for the photograph.
    def generateSampleLabel(self) ->str:
        '''This method generates the label for the photograph. It is used to label the photographs with the name of the person and the date of the photograph.'''

        # generates the label for the photograph
        label ='_'.join( self.__projectName , self.__typeMaterial , self.__sampleNumber)

        # returns the label for the photograph
        return label
    
    # genererates label for the augmented data
    def generateAugmentedLabel(self)->str:
        '''this method generates the label for the augmented photographs. It uses the sample label as basis'''

        # generates the label for the augmented data
        label='_'.join( self.__projectName , self.__typeMaterial , self.__sampleNumber,self.__AugmentedNumber)

        # returns the label
        return label