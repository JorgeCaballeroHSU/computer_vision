# this class is used for the definition of the socket in the server-side

# imports required libraries
import socket

# defines the class SocketServer, which is used to create a socket server
class SocketServer:

    # properties of the class SocketServer

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
    def accept(self)->tuple:
        '''accepts an incoming connection

        Returns:
            Socket: a new Socket object representing the accepted connection
            tuple: the address of the client that made the connection
        '''

        # accepts an incoming connection and returns a new Socket object and the client's address
        return SocketServer(self.sock.accept()[0]), self.sock.accept()[1]

    # method to send data through the socket
    def send(self, data)->None:
        '''sends data through the socket
        Args:
            data (str): the data to be sent

        Returns:
            None
        '''

        # sends the data through the socket
        self.sock.sendall(data.encode())

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

        # receives data from the socket
        data = self.sock.recv(bufferSize).decode()

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
    