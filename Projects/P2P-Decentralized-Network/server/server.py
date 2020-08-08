#######################################################################################
# File:             server.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template Server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this server class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           server = Server() # creates object
########################################################################################

import sys
import socket
from threading import Thread, Event
import pickle
from client_handler import ClientHandler


class Server(object):
    CLIENT_MIN_PORT_RANGE = None
    CLIENT_MAX_PORT_RANGE = None

    def __init__(self, ip_address, port, id_key):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # set server info variables
        self.ip_address = ip_address
        self.port = port
        self.id_key = id_key
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((self.ip_address, self.port))

    def listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        try:
            self.serversocket.listen()
            # print server listening message
            print("[" + self.id_key + " SERVER] Listening at " + self.ip_address + "/" + str(self.port))
        except:
            # handle exception
            print("Failed at server binding / listening: ", sys.exc_info()[0])
            self.serversocket.close()
            raise

    def accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # Accept a client
                clientsocket, addr = self.serversocket.accept()
                clientsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
                clientsocket.settimeout(0.01)
                # Create a thread of this client using the client_handler_thread class
                Thread(
                    target=self.client_handler_thread,
                    args=(clientsocket, addr)
                    ).start()
            except KeyboardInterrupt:
                # handle control+c
                break
            except:
                # Handle exceptions
                print("Failed at accepting / threading client: ", sys.exc_info()[0])
                raise

    def send(self, clientsocket, data):
        """
        Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return: VOID
        """
        print("[" + self.id_key + " SERVER] ### DEBUG # SENT -- START") #debug
        print(data) #debug
        print("[" + self.id_key + " SERVER] ### DEBUG # SENT -- END") #debug
        # creates a stream of bytes
        serialized_data = pickle.dumps(data)
        while True:
            try:
                # data sent to the client
                clientsocket.sendall(serialized_data)
            except socket.timeout:
                continue
            else:
                break

    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        raw_data = b''
        # server receives data (even splitted)
        while True:
            try:
                fragment = clientsocket.recv(MAX_BUFFER_SIZE)
                if not fragment:
                    break
                raw_data += fragment
                if len(fragment) < MAX_BUFFER_SIZE:
                    break
            except socket.timeout:
                continue
        if not raw_data:
            return None
        # deserializes the data received
        deserialized_data = pickle.loads(raw_data)
        print("[" + self.id_key + " SERVER] ### DEBUG # RECEIVED -- START") #debug
        print(deserialized_data) #debug
        print("[" + self.id_key + " SERVER] ### DEBUG # RECEIVED -- END") #debug
        return deserialized_data

    def client_handler_thread(self, clientsocket, address):
        raise NotImplementedError

    def timed_connection(self, time=None):
        raise NotImplementedError

    def connect(self, ip_address, client_port_to_bind, path):
        raise NotImplementedError

    def connect_all_thread(self, urls):
        """
        Initialize a temporal variable to the min client port range, then
        For each client ip address, call the method connect() method, and
        increment the client's port range that needs to be bind to the next client.
        Break the loop when the port value is greater than the max client port range.
        :param urls: list of client's urls in the network
        :return: VOID
        """
        client_port = self.CLIENT_MIN_PORT_RANGE
        for url in urls:
            # check if client_port is out of range
            if client_port > self.CLIENT_MAX_PORT_RANGE:
                break
            # increment client_port if client is connected
            if self.connect(*url):
                client_port += 1

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self.listen()
        try:
            # make a nonblocking accept client thread
            Thread(
                target=self.accept_clients,
                args=()
                ).start()
        except:
            # Handle exceptions
            print("Failed at threading server: ", sys.exc_info()[0])
            raise
