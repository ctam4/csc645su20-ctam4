#######################################################################################
# File:             client.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template Client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           client = Client() # creates object
########################################################################################

import socket
import pickle
import sys


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self, server):
        """
        Class constructor
        :param id_key:
        :return: VOID
        """
        self.server = server
        self.ip_address = self.server.ip_address
        self.port = self.server.port
        self.id_key = self.server.id_key
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.clientsocket.settimeout(0.01)
        # bind on client created
        #self.bind()

    def bind(self):
        """
        Bind for client
        :param ip_address:
        :param port:
        :return: VOID
        """
        try:
            self.clientsocket.bind((self.ip_address, self.port))
        except:
            # handle exception
            print("Failed at client binding: ", sys.exc_info()[0])
            self.close()
            raise

    def connect(self, ip_address, port, path):
        raise NotImplementedError

    def send(self, data, MAX_BUFFER_SIZE=4096):
        """
        Serializes and then sends data to server
        :param data:
        :return: VOID
        """
        print("[" + self.id_key + " CLIENT] ### DEBUG # SENT -- START") #debug
        print(data) #debug
        print("[" + self.id_key + " CLIENT] ### DEBUG # SENT -- END") #debug
        # creates a stream of bytes
        serialized_data = pickle.dumps(data)
        while True:
            try:
                # data sent to the server
                self.clientsocket.sendall(serialized_data)
            except socket.timeout:
                continue
            else:
                break

    def receive(self, MAX_BUFFER_SIZE=4096):
        """
        Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = b''
        # client receives data (even splitted)
        while True:
            try:
                fragment = self.clientsocket.recv(MAX_BUFFER_SIZE)
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
        print("[" + self.id_key + " CLIENT] ### DEBUG # RECEIVED -- START") #debug
        print(deserialized_data) #debug
        print("[" + self.id_key + " CLIENT] ### DEBUG # RECEIVED -- END") #debug
        return deserialized_data

    def process(self):
        raise NotImplementedError

    def close(self):
        """
        close the client socket
        :return: VOID
        """
        self.clientsocket.close()
