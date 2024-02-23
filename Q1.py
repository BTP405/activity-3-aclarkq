#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.

#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.

import socket
import pickle
import os
import sys
import threading

port = 25565
address = 'localhost'
        
def directory_selector(str_type):
    """ Selects directory

    Args:
        str_type (str): "saved at" or "stored" for type of directory.

    Returns:
        str: file path
    """
    print("Enter the directory where the data is" + str_type)
    directory = input()
    
    # Check if directory exists and is not empty
    if os.path.exists(directory) and os.listdir(directory):
        return directory
    else:
        print("Directory does not exist or is empty. Please try again.")
        directory_selector(str_type)
        
def list_files(directory):
    """ Lists files in directory

    Args:
        directory (str): directory

    Returns:
        str: file path
    """
    files = os.listdir(directory) # Get files in directory
    
    # Assign files to a dictionary
    filecount = 0
    files_dict = {}
    for file in files:
        files_dict[filecount] = directory + "/" + file
        filecount += 1
        
    # Display files to user
    for key, value in files_dict.items():
        print(str(key) + " : " + value)
        
    return files_dict
             
def run_client(address, port):
    """Runs the client.

    Args:
        address (str): The address of the server.
        port (int): The port of the server.
    """
    # initialize TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    client_socket.connect(server_address)

    print(f"Client is connected to {address}:{port}")

    try:
        # Use the directory_selector function to get a valid directory
        directory = directory_selector("stored")

        # Use the list_files function to list and get files in the directory
        files_dict = list_files(directory)

        # Get file number from user
        file_num = input("Enter the file number corresponding to the file you want to send: ")

        # Get file path from dictionary
        file_path = files_dict[file_num]

        # Read the file content
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Create a dictionary to hold file information
        file_data = {'name': file_path.split('/')[-1], 'content': file_content}

        # Pickle the file object
        pickled_data = pickle.dumps(file_data)

        # Send the pickled file object
        client_socket.sendall(pickled_data)

        print("File sent successfully")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
    

def receive_file(client_socket, save_directory):
    """Receives the pickled file object and saves it to disk.

    Args:
        client_socket (socket): The client socket.
        save_directory (str): The directory to save the file.
    """
    try:
        # Receive the pickled file object
        data = client_socket.recv(4096)
        if not data:
            print("Error: No data received.")
            return

        # Unpickle the file object
        file_data = pickle.loads(data)

        # Extract file information
        file_name = file_data['name']
        file_content = file_data['content']

        # Save the file to the specified directory
        file_path = os.path.join(save_directory, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_content)

        print(f"File received and saved to {file_path}")

    except Exception as e:
        print(f"Error: {e}")

def run_server(address, port):
    """Runs the server.

    Args:
        address (str): The address of the server.
        port (int): The port of the server.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"Server is listening on {address}:{port}")

    try:
        # Use the directory_selector function to get a valid directory
        save_directory = directory_selector("saved at")

        # Infinite loop for waiting for a connection
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Use the receive_file function to handle file reception
            receive_file(client_socket, save_directory)

            client_socket.close()

    except Exception as e:
        print(f"Server Error: {e}")

    finally:
        server_socket.close()
    
if __name__ == "__main__": # If the code is run as the main program (not as an import)
    if len(sys.argv) != 2: # Check if the number of arguments is correct; if not:
        print("Usage: python Q1.py <server|client>")
        sys.exit(1)

    mode = sys.argv[1].lower() # Get the mode from the command line argument

    if mode == 'server':
        # Run the server in a separate thread
        server_thread = threading.Thread(target=run_server, args=('127.0.0.1', 5555))
        server_thread.start()

    elif mode == 'client':
        # Run the client in the main thread
        run_client('127.0.0.1', 5555)

    else:
        print("Invalid mode. Use 'server' or 'client'.")
        sys.exit(1)