import sys
import pickle
import socket


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """

    def __init__(self, ready, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param ready: thread ready lock
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.ready = ready
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.ready.set()

    def run(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def delete_client_data(self):
        """
        delete all the data related to this client from the server.
        :return: VOID
        """
        # remove from server current client list
        self.server.clients.pop(self.client_id)

    def disconnect_from_server(self):
        """
        call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        # send goodbye message
        self.clientsocket.close()
        return False
