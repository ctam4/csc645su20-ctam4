########################################################################################################################
# Class: Computer Networks
# Date: 06/30/2020
# Lab4: Threading clients in server side
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Calvin Tam
# Student ID: 917902523
# Student Github Username: ctam4
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################

import threading
import pickle
class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param clientsocket: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.handler = clientsocket
        self.print_lock = threading.Lock() # creates the print lock

    def process_client_data(self):
        """
        TODO: receives the data from the client
        TODO: prepares the data to be printed in console
        TODO: acquire the print lock
        TODO: prints the data in server console
        TODO: release the print lock
        TODO: keep this handler object listening for more incoming data from the client
        :return: VOID
        """
        while True:
             # TODO: receive data from client
             # TODO: if no data, break the loop
             # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data
             data = self.receive() # receives data from this client
             self.print_lock.acquire()
             print("Received data from client " + str(self.client_id) + ": " + str(data))
             self.print_lock.release()
             #status = {'message': "server got the data"}
             #self.print_lock.acquire()
             #print("Sending acknowledge to client " + str(self.client_id) + ": " + str(status))
             #self.print_lock.release()
             #self.send(status)

    def send_clientid(self):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        client_id = {'clientid': self.client_id}
        self.send(client_id)

    def send(self, data):
        serialized_data = pickle.dumps(data) # creates a stream of bytes
        self.handler.send(serialized_data) # data sent to the client.

    def receive(self, MAX_ALLOC_MEM=4096):
        # server receives data
        data_from_client = self.handler.recv(MAX_ALLOC_MEM)
        if not data_from_client:
            return None
        # deserializes the data received
        serialized_data = pickle.loads(data_from_client)
        return serialized_data #change the return value after implemente.

    def run(self):
        # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
        self.send_clientid()
        self.process_client_data()
