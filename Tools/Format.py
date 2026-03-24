# it contains a function that adds the data-tpye to the name of the file

# adds the data type to the file name
def addDataType(fileName:str,dataType:str='')->str:

    # checks if the dataType attribute is empty
    if dataType=='':

        # informs that no data type was provided
        print('No data type was provided. Please, provide one!')

        # returns the fileName
        return fileName
    
    # if the dataType attribute is not empty, then join it with the fileName
    else:

        # returns the file name with its data type
        return '.'.join(fileName,dataType)
