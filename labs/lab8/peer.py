"""
Lab 8: peer.py
This file contains a basic template of the Peer class. In this lab, your job 
is to implement all the parts marked as TODO. Note that you don´t need to run
the code of this lab. The goal of this lab is to see how your logic works, and
therefore, to make sure that you understood how peers perform the downloading 
and uploading process in the network, and also which challenges you may encounter
when implementing those functionalities. 
"""
from server import Server # assumes that your server file is in this folder
from client import Client # assumes that your client file is in this folder
from tracker import Tracker  # assumes that your Tracker file is in this folder
class Peer:

    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010

    def __init__(self):
       self.server = None
       self.run_server() # starts the server
       self.run_tracker(self.server)

    def run_server(self):
        """
        TODO: 1. Create and run a threaded server object 
        """
        pass # your code here
    
    def run_tracker(server):
        """
        TODO: 1. Create and run a threaded tracker
        :param server: the server instance. 
        """
        if server:
            pass # your code here
    
    def _connect_to_peer(self, client_port_to_bind, peer_ip_address):
        """
        TODO: Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that
                                the client needs to connect to
        :return: VOID
        """
        try:
            pass # your code here
        except:
            pass # handle exceptions here

    def connect(self, peers_ip_addresses):
        """
        TODO: Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
        pass # your code here

