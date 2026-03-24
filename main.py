# main.py

# imports required libraries
from Sockets.SocketServer import SocketServer
from dataBaseFill import dataBaseFill
from trainModel import trainModel
from prediction import prediction


# connects with the client

# gets from the client the next step 
# there are four possibilities
# fill up the database, train the model, make a prediction, or close
clienteRequest=1

# loops through the menu possibilities
while True:

    # if the answer of the client is 0, then database if to be filled
    if clienteRequest==0:

        # calls the function to fill up the database
        answerFromFunction=dataBaseFill()

        # prints the results of this process
        print(answerFromFunction)

    # if the answer of the client is 1, then the model is to be trianed
    elif clienteRequest==1:
        
        # cakks the function to train the model
        answerFromFunction=trainModel()

        # prints the results of this process
        print(answerFromFunction)

    # if the answer of the client is 2, then a prediction if to be provided
    elif clienteRequest==2:  

        # calls the function to obtain a prediction
        answerFromFunction=prediction()

        # prints the answer of the prediction function
        print(answerFromFunction)
    
    # anything else, the loops breaks and the system ends
    else:

        break

    

