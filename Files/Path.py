# this files is used to get and set the path of the photographs.

# imports the necessary libraries
import os

# creates class for the path of the photographs
class Path:
    
    '''This class is in charge of the path of the photographs according to the conventions of the project. It is used to get and set the path of the photographs.'''

    # properties of the class
    __path: str = ""

    # methods of the class
    def __init__(self) ->None:

        # checks if the properties of the class are empty
        if self.__path == "":
            
            # if the properties of the class are empty, tries to download the properties of the class from the database
            boolValue = self.downloadProperties()

            #if self.downloadProperties() == False, then the properties are still empty
            if boolValue == False:
                pass
            else:
                # if the properties of the class are not empty, then the properties of the class are downloaded from the database
                pass
        pass

    # loads the path of the photographs from the database
    def loadPath(self) ->None:
        
        '''This method loads the path of the photographs from the database. It is used to get and set the path of the photographs.'''

        # code to load the path of the photographs from the database goes here

        # returns nothing
        return None

    # saves the path of the photographs to the database
    def savePath(self) ->None:
        
        '''This method saves the path of the photographs to the database. It is used to get and set the path of the photographs.'''

        # code to save the path of the photographs to the database goes here

        # returns nothing
        return None

    # gets the path of the photographs
    def getPath(self) ->str:

        '''This method gets the path of the photographs. It is used to get and set the path of the photographs.'''

        # returns the path of the photographs
        return self.__path

    # sets the path of the photographs
    def setPath(self, path: str) ->None:

        '''This method sets the path of the photographs. It is used to get and set the path of the photographs.'''

        # sets the path of the photographs
        self.__path = path

        # returns nothing
        return None