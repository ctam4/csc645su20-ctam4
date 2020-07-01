########################################################################################################################
# Class: Computer Networks
# Date: 06/30/2020
# Lab4: Threading clients in server side
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Calvin Tam
# Student ID: 917902523
# Student Github Username: ctam4
# Lab Instructions: No partial credit will be given in this lab
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import sys
import socket
import pickle
from threading import Thread
from client_handler import ClientHandler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port = 12000):
        """
        Class constructor
        # TODO: create the server socket
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_handlers = {}

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            # your code here
            self.serversocket.listen()
            print("Server listening at " + str(self.host) + "/" + str(self.port))
        except:
            print("Failed at server binding or listening:", sys.exc_info()[0])
            self.serversocket.close()
            raise

    def threaded_client(self, clientsocket, addr):
        client_id = addr[1]
        client_handler = ClientHandler(self, clientsocket, addr) # self is the server instance
        client_handler.run() # inits all the components in client handler object
        #  adds the client handler object to the list of all the clients objects created by this server.
        #  key: client id, value: client handler
        self.client_handlers[client_id] = client_handler # assumes dict was initialized in class constructor

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               clientsocket, addr = self.serversocket.accept()
               Thread(target=self.threaded_client, args=(clientsocket, addr)).start() # client thread started
            except:
               # handle exceptions here
               print("Failed at accepting / threading client:", sys.exc_info()[0])
               raise

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
