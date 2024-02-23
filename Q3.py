#Real-Time Chat Application with Pickling:

#Develop a simple real-time chat application where multiple clients can communicate with each other via a central server using sockets. 
#Messages sent by clients should be pickled before transmission. The server should receive pickled messages, unpickle them, and broadcast them to all connected clients.

#Requirements:
#Implement separate threads for handling client connections and message broadcasting on the server side.
#Ensure proper synchronization to handle concurrent access to shared resources (e.g., the list of connected clients).
#Allow clients to join and leave the chat room dynamically while maintaining active connections with other clients.
#Use pickling to serialize and deserialize messages exchanged between clients and the server.

import socket
import threading
import pickle

class ChatServer:
    """
    A simple real-time chat application where multiple clients can communicate with each other via a central server using sockets.
    Messages sent by clients are pickled before transmission. The server receives pickled messages, unpickles them, and broadcasts them to all connected clients.

    Args:
        host (str): The host address of the server.
        port (int): The port number of the server.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def broadcast(self, message, client_socket):
        """
        Broadcasts a message to all connected clients.

        Args:
            message (str): The message to be broadcast.
            client_socket (socket.socket): The socket of the client that sent the message.
        """
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(pickle.dumps(message))
                except:
                    # Remove the client if there's an issue with sending the message
                    self.remove_client(client)

    def remove_client(self, client_socket):
        """
        Removes a client from the list of connected clients.

        Args:
            client_socket (socket.socket): The socket of the client to be removed.
        """
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def handle_client(self, client_socket, addr):
        """
        Handles a client connection.

        Args:
            client_socket (socket.socket): The socket of the client.
            addr (tuple): The address of the client.
        """
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Unpickle the message
                message = pickle.loads(data)
                # Broadcast the message to all connected clients
                self.broadcast(message, client_socket)
        except:
            pass  # Handle disconnection or errors
        finally:
            client_socket.close()
            self.remove_client(client_socket)

    def start(self):
        """
        Starts the server.
        """
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                
                # Add the client to the list of connected clients
                self.clients.append(client_socket)
                
                print("Client connected:", addr)
                
                # Broadcast that a new client has joined
                message = f"{self.username} has joined the chat."
                self.broadcast(message, client_socket)
                
                # Start a new thread to handle the client
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

class ChatClient:
    """
    A simple real-time chat application where multiple clients can communicate with each other via a central server using sockets.
    Messages sent by clients are pickled before transmission. The server receives pickled messages, unpickles them, and broadcasts them to all connected clients.

    Args:
        host (str): The host address of the server.
        port (int): The port number of the server.
        username (str): The username of the client.
    """

    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, message):
        """
        Sends a message to the server.

        Args:
            message (str): The message to be sent.
        """
        try:
            self.client_socket.send(pickle.dumps(f"{self.username}: {message}"))
        except:
            print("Error sending message.")

    def receive_messages(self):
        """
        Receives messages from the server.
        """
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = pickle.loads(data)
                print(message)
        except:
            pass  # Handle disconnection or errors
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    # Execute both server and client from the same script
    is_server = input("Are you running as a server? (y/n): ").lower() == 'y'

    if is_server:
        host = input("Enter server host (default: 127.0.0.1): ") or "127.0.0.1"
        port = int(input("Enter server port (default: 25565): ") or 25565)
        server = ChatServer(host, port)
        server.start()
    else:
        host = input("Enter server host (default: 127.0.0.1): ") or "127.0.0.1"
        port = int(input("Enter server port (default: 25565): ") or 25565)
        username = input("Enter your username: ")
        client = ChatClient(host, port, username)
        while True:
            message = input("Enter your message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client.send_message(message)
