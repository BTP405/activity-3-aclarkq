import socket
import pickle
import threading
import queue

"""
A task queue that stores tasks and provides methods to add and get tasks.
"""
class TaskQueue:
    def __init__(self):
        """
        Initializes a task queue.
        """
        self.tasks = queue.Queue()

    def add_task(self, task):
        """
        Adds a task to the queue.

        Args:
            task: The task to add.
        """
        self.tasks.put(task)

    def get_task(self):
        """
        Gets a task from the queue.

        Returns:
            The task, or None if the queue is empty.
        """
        if not self.tasks.empty():
            return self.tasks.get()
        return None

"""
A worker node that listens for tasks from a client and executes them.
"""
class WorkerNode:
    def __init__(self, host, port, task_queue):
        """
        Initializes a worker node.

        Args:
            host: The host address of the worker node.
            port: The port number of the worker node.
            task_queue: The task queue to get tasks from.
        """
        self.host = host
        self.port = port
        self.task_queue = task_queue

    def start(self):
        """
        Starts the worker node.
        """
        # Create a socket and bind it to the host and port
        # Code is referenced from https://realpython.com/python-sockets/
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            
            print(f"Worker node listening on {self.host}:{self.port}")
            # Start listening for incoming connections
            sock.listen()

            while True:
                # Accept a connection
                conn, addr = sock.accept()
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        break
                    task = pickle.loads(data)
                    result = self.execute_task(task)
                    conn.sendall(pickle.dumps(result))

    def execute_task(self, task):
        """
        Executes a task.

        Args:
            task: The task to execute.

        Returns:
            The result of the task.
        """
        function, args = task
        try:
            result = function(*args)
            print("Node executed task: " + str(result))
            return result
        except Exception as e:
            return f"Error: {str(e)}"

"""
A client that distributes tasks to worker nodes and collects the results.
"""
class Client:
    def __init__(self, worker_nodes):
        """
        Initializes a client.

        Args:
            worker_nodes: A list of worker nodes.
        """
        print("Client initialized")
        self.worker_nodes = worker_nodes

    def distribute_tasks(self, tasks):
        """
        Distributes tasks to worker nodes.

        Args:
            tasks: A list of tasks.

        Returns:
            A list of results.
        """
        results = []
        threads = []

        for task in tasks:
            print("Getting available node")
            node = self.get_available_node()
            if node:
                thread = threading.Thread(target=self.execute_task_on_node, args=(node, task, results))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        return results

    def get_available_node(self):
        """
        Gets an available worker node.

        Returns:
            A worker node, or None if no available node is found.
        """
        for node in self.worker_nodes:
            return node
        return None

    def execute_task_on_node(self, node, task, results):
        """
        Executes a task on a worker node.

        Args:
            node: The worker node to execute the task on.
            task: The task to execute.
            results: A list to store the results.
        """
        result = node.execute_task(task)
        results.append(result)

"""
A node that can execute tasks.
"""
class Node:
    def __init__(self, host, port):
        """
        Initializes a node.

        Args:
            host: The host address of the node.
            port: The port number of the node.
        """
        self.host = host
        self.port = port

    def execute_task(self, task):
        """
        Executes a task.

        Args:
            task: The task to execute.

        Returns:
            The result of the task.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps(task))
            data = s.recv(4096)
            return pickle.loads(data)

"""
A worker that can execute tasks and report its availability.
"""
class Worker(Node):
    def __init__(self, host, port, task_queue):
        """
        Initializes a worker.

        Args:
            host: The host address of the worker.
            port: The port number of the worker.
            task_queue: The task queue to get tasks from.
        """
        super().__init__(host, port)
        self.task_queue = task_queue

    def start(self):
        """
        Starts the worker.
        """
        while True:
            task = self.task_queue.get_task()
            if task:
                result = self.execute_task(task)
                print(f"Task result: {result}")

# Example usage
if __name__ == "__main__":
    task_queue = TaskQueue()

    worker_nodes = [WorkerNode("localhost", 5001, task_queue)]

    for worker_node in worker_nodes:
        threading.Thread(target=worker_node.start).start()

    client = Client([Node("localhost", 5001)])
    
    # Example tasks
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    tasks = [(add, (1, 2)), (multiply, (3, 4)), (add, (5, 6))]

    for task in tasks:
        task_queue.add_task(task)
        print("Added task: " + str(task))

    results = client.distribute_tasks(tasks)
    print(f"Final Results: {results}")
