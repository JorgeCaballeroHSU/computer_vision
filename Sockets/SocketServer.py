# this class is used for the definition of the socket in the server-side
######### maybe change this to webSockets
# imports required libraries
import socket

# defines the class SocketServer, which is used to create a socket server
class SocketServer():

    # properties of the class SocketServer
    __conn:socket
    __addr:None

    # constructor of the class SocketServer, it initializes the socket object
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    # method to bind the socket to a specific address and port
    def bind(self, host, port)->None:
        '''binds the socket to a specific address and port
        Args:
            host (str): the address to bind the socket to
            port (int): the port to bind the socket to
        
        Returns:
            None
        '''

        # binds the socket to the specified host and port
        self.sock.bind((host, port))

        # returns None
        return None
    
    # method to listen for incoming connections
    def listen(self, backlog=5)->None:
        '''listens for incoming connections
        Args:
            backlog (int, optional): the maximum number of queued connections. Defaults to 5.

        Returns:
            None
        '''

        # makes the socket listen for incoming connections
        self.sock.listen(backlog)

        # returns None
        return None
    
    # method to accept an incoming connection
    def accept(self)->None:
        '''accepts an incoming connection

        Returns:
            None
        '''

        # accepts an incoming connection. Gets the connection and address
        self.__conn, self.__addr=self.sock.accept()
        
        #returns None
        return None

    # method to send data through the socket
    def send(self,toSend:str)->None:
        '''sends data through the socket
        Args:
            data (str): the data to be sent

        Returns:
            None
        '''

        # sends the data through the socket
        #with self.__conn:

            # informs about the address of the connection
        print("Connected by {}".format(self.__addr))

            #while opp for sending the data through the socket
            #while True:

                #data=self.__conn.recv(1024)

                #print(data)
                # if not data:
                #     break
                
        self.__conn.sendall(toSend.encode())

        #    data
        # returns None
        return None
    
    # method to receive data from the socket
    def receive(self, bufferSize=1024)->str:
        '''receives data from the socket
        Args:
            bufferSize (int, optional): the maximum amount of data to be received at once. Defaults to 1024.

        Returns:
            str: the data received from the socket
        '''
        # while loop to receive the information
        while True:

            # receives data from the socket
            data = self.__conn.recv(bufferSize).decode()
            
            # prints the results
            print(data)

            # check if there is new data coming
            if not self.__conn.recv(bufferSize).decode():
                
                # breaks the loop
                break
            
            

        # returns the received data
        return data
    
    # method to close the socket
    def close(self)->None:
        '''closes the socket

        Returns:
            None
        '''

        # closes the socket
        self.sock.close()

        # returns None
        return None
    

# server=SocketServer()

# server.bind(
#     host='0.0.0.0',
#     port=5000
# )

# server.listen()
# server.accept()

# server.send(toSend='Hola')
# # a=server.receive()

