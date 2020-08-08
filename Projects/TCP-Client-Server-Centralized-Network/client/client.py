#######################################################################
# File:             client.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python client.py
#                   Python 3: python3 client.py
########################################################################

import sys
import socket
import pickle


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constructor
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.clientsocket.settimeout(0.01)
        self.clientid = 0

    def set_client_id(self):
        """
        Sets the client id assigned by the server to this client after a succesfull connection
        :return:
        """
        # deserialized data
        data = self.receive()
        # extracts client id from data
        client_id = data['clientid']
        # sets the client id to this client
        self.clientid = client_id

    def get_client_id(self):
        return self.clientid

    def client_info(self, id_key):
        data = {'id_key': id_key}
        self.send(data)

    def connect(self, ip_address="127.0.0.1", port=12005):
        """
        Connects to a server. Implements exception handler if connection is resetted.
	    Then retrieves the cliend id assigned from server, and sets
        :param ip_address:
        :param port:
        :return: VOID
        """
        try:
            # get user inputs for connection info
            while True:
                try:
                    user_input = input("Enter the server IP Address (Default: " + ip_address + "): ")
                    if not user_input:
                        break
                    else:
                        socket.inet_aton(user_input)
                except socket.error:
                    print("Not a valid IP Address!")
                else:
                    ip_address = user_input or ip_address
                    break
            while True:
                try:
                    user_input = input("Enter the server port (Default: " + str(port) + "): ")
                    if not user_input:
                        break
                    else:
                        user_input = int(user_input)
                        if user_input <= 0 or user_input > 65535:
                            print("Not a valid port!")
                            continue
                except ValueError:
                    print("Not a valid port!")
                else:
                    port = user_input or port
                    break
            while True:
                id_key = input("Your id key (i.e your name): ")
                if id_key:
                    break
            # use the self.client to create a connection with the server
            self.clientsocket.connect((ip_address, port))
            # print connected message
            print("Successfully connected to server: " + ip_address + "/" + str(port))
            # once the client creates a successful connection, the server will send the client id to this client.
            # call the method set_client_id() to implement that functionality.
            self.set_client_id()
            # send client info
            self.client_info(id_key)
            # print client info
            print("Your client info is:")
            print("Client Name: " + id_key)
            print("Client ID: #" + str(self.get_client_id()))
            # client is put in listening mode to retrieve data from server.
            while True:
                data = self.receive()
                if data:
                    self.process(data)
        except KeyboardInterrupt:
            # handle control+c
            pass
        except:
            # handle exception
            print("Failed at client connecting or during active connection: ", sys.exc_info()[0])
            self.close()
            raise
        else:
            # print disconnect message
            print("Disconnected from server. Bye.")

    def send(self, data, MAX_BUFFER_SIZE=4096):
        """
        Serializes and then sends data to server
        :param data:
        :return: VOID
        """
        # creates a stream of bytes
        serialized_data = pickle.dumps(data)
        while True:
            try:
                # data sent to the server
                self.clientsocket.sendall(serialized_data)
                # # check acknowledge
                # try:
                #     raw_data = self.clientsocket.recv(MAX_BUFFER_SIZE)
                #     if not raw_data:
                #         print("Incomplete data submission.")
                #     deserialized_ack = pickle.loads(raw_data)
                #     print(deserialized_ack)
                #     if not deserialized_ack['received'] == len(serialized_data):
                #         print("Incomplete data submission (" + str(deserialized_ack['received']) + " received, " + str(len(serialized_data)) + "sent).")
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
        # # send acknowledge if this is not acknowledge
        # if not 'received' in deserialized_data.keys():
        #     ack = {'received': len(raw_data)}
        #     print(ack) #debug
        #     serialized_ack = pickle.dumps(ack)
        #     self.clientsocket.sendall(serialized_ack)
        return deserialized_data

    def process(self, data):
        """
        Process received data and user prompts
        :param data:
        :return: VOID
        """
        if 'menu' in data.keys():
            print("\n" + data['menu'])
            while True:
                try:
                    user_input = input("\nYour option <enter a number>: ")
                    if not user_input:
                        continue
                    else:
                        user_input = int(user_input)
                        if user_input <= 0 or user_input > 6:
                            print("Not a valid option!")
                            continue
                except ValueError:
                    print("Not a valid option!")
                else:
                    # ready return message
                    res = {'option_selected': user_input}
                    # send return message to server
                    self.send(res)
                    break
        elif 'option' in data.keys() and 'params' in data.keys():
            if 'output' in data.keys():
                print("\n" + data['output'])
            if len(data['params']) > 0:
                print()
                user_input = data['input']
                for i in data['params']:
                    user_input[i] = input(data['input'][i])
                # ready return message
                res = {
                    'option': data['option'],
                    'params': data['params'],
                    'input': user_input
                }
                # send return message to server
                self.send(res)

    def close(self):
        """
        close the client socket
        :return: VOID
        """
        self.clientsocket.close()


if __name__ == '__main__':
    client = Client()
    client.connect()
