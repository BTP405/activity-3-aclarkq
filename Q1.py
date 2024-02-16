#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.

#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.

import socket
import socketserver
import pickle
import sys
import os

port = 25565
address = 'localhost'

def run_server():
    """
    Starts the server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    
    print("Server is listening on {address}:{port}")
    
    #while loop for waiting for a connection
    while True:
        client_socket, clientaddress = server_socket.accept()
        
        
        
def run_client(address, port):
    # initialize TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    client_socket.connect(server_address)
    
    print("Client is connected to {address}:{port}")
    
    # Get directory from user
    print("Enter a directory")
    directory = input()
    
    files = os.listdir(directory) # Get files in directory
    
    # Assign files to a dictionary
    filecount = 0
    files_dict = {}
    for file in files:
        files_dict[filecount] = directory + "/" + file
        filecount += 1
        
    # Display files to user
    for key, value in files_dict.items():
        print(key + " : " + value)
        
    # Get file number from user
    print("Enter a file number")
    file_num = input()
    
    pickledFile = pickle_file(files_dict[int(file_num)]) # Pickle selected file
    
    
    
    client_socket.close() # Close connection


def pickle_file(file_path):
    """ Pickles file; creates a new (pickled) file in the same directory as the original
        Calls read_file_to_object to pickle

    Args:
        file_path (string): Path to file to be pickled
        
    Returns:
        string: Path to new (pickled) file
    """
    # Create new file
    file = open(file_path, 'rb') # Open file
    file_object = file.read() # Read file
    file.close() # Close file
    
    
    
    

def unpickle_file():
    """ Unpickles file """
    pass


    
     

