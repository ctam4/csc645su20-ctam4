#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

import sys
from builtins import object
import socket
from threading import Thread, Event
import pickle
from client_handler import ClientHandler


class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, ip_address="127.0.0.1", port=12005):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # set server info variables
        self.ip_address = ip_address
        self.port = port
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.chatrooms = {}
        # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((self.ip_address, self.port))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        try:
            self.serversocket.listen()
            # print server listening message
            print("Server listening at " + self.ip_address + "/" + str(self.port))
        except:
            # handle exception
            print("Failed at server binding or listening: ", sys.exc_info()[0])
            self.serversocket.close()
            raise

    def _accept_clients(self):
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
                print("Failed at accepting / threading client:", sys.exc_info()[0])
                raise

    # def send_ack(self, clientsocket, n, MAX_BUFFER_SIZE=4096):
    #     """
    #     Send acknowledge
    #     :param clientsocket:
    #     :param n: size of serialized data
    #     :return: VOID
    #     """
    #     ack = {'received': n}
    #     print(ack) #debug
    #     serialized_ack = pickle.dumps(ack)
    #     clientsocket.sendall(serialized_ack)
    #
    # def receive_ack(self, clientsocket, n):
    #     """
    #     Receive and validate acknowledge
    #     :param clientsocket:
    #     :param n: size of sent serialized data
    #     :return: BOOLEAN
    #     """
    #     if not n in self.acknowledges:
    #         print("Incomplete data submission (" + str(n) + "sent).")

    def send(self, clientsocket, data):
        """
        Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return: VOID
        """
        print("### send -- start") #debug
        print(data) #debug
        print("### send -- end") #debug
        # creates a stream of bytes
        serialized_data = pickle.dumps(data)
        while True:
            try:
                # data sent to the client
                clientsocket.sendall(serialized_data)
                # # check acknowledge
                # try:
                #     if not receive_ack(clientsocket, n):
                #         continue
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
        print("### received -- start") #debug
        print(deserialized_data) #debug
        print("### received -- end") #debug
        # # send acknowledge if this is not acknowledge
        # if not 'received' in deserialized_data.keys():
        #     send_ack(clientsocket, len(raw_data))
        #     return deserialized_data
        # else:
        #     receive_ack(clientsocket, len(raw_data))
        return deserialized_data

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        # threading event
        ready = Event()
        # create a new client handler object and return it
        # inits all the components in client handler object
        # self is the server instance
        client_handler = ClientHandler(ready, self, clientsocket, address)
        # adds the client handler object to the list of all the clients objects created by this server.
        # key: client id, value: client handler
        # assumes dict was initialized in class constructor
        self.clients[client_handler.client_id] = client_handler
        # start client handler engine when it is ready
        ready.wait()
        client_handler.run()
        return client_handler

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()
