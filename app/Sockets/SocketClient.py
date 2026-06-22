# this files contains the implementation of the SocketClient class, which is used to create a socket client that can connect to a socket server and send data through the socket

# imports required libraries
import socket

# defines the class SocketClient, which is used to create a socket client
class SocketClient:

    # properties of the class SocketClient

    # constructor of the class SocketClient, it initializes the socket object
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    # method to connect to a socket server
    def connect(self, host: str, port: int)->None:
        '''connects to a socket server
        Args:
            host (str): the address of the socket server to connect to
            port (int): the port of the socket server to connect to
        
        Returns:
            None
        '''

        # connects to the specified host and port
        self.sock.connect((host, port))

        # returns None
        return None
    
    # method to send data through the socket
    def send(self, data: str)->None:
        '''sends data through the socket
        Args:
            data (str): the data to send through the socket
        
        Returns:
            None
        '''

        # sends the specified data through the socket
        self.sock.sendall(data.encode())

        # returns None
        return None
    
    # method to receive data from the socket
    def receive(self, bufferSize: int = 1024) -> str:
        '''receives data from the socket
        Args:
            bufferSize (int, optional): the maximum amount of data to receive at once. Defaults to 1024.

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
    