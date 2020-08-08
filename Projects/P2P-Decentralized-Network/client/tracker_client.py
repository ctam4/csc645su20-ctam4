#######################################################################################
# File:             tracker_client.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template Client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           tracker_client = TrackerClient() # creates object
########################################################################################

import socket
import pickle
import re
import sys

sys.path.insert(0, './thp')

from client import Client
from thp import THP


class TrackerClient(Client):
    def __init__(self, server):
        """
        Inhert __init__ from base class and process new parameter
        :param id_key:
        :param torrent_info_hash:
        :return: VOID
        """
        super().__init__(server)
        self.torrent_info_hash = self.server.torrent_info_hash
        # init THP
        self.thp = THP()

    def connect(self, ip_address, port, path=None):
        """
        Connects to a server. Implements exception handler if connection is resetted.
	    Then retrieves the cliend id assigned from server, and sets
        :param ip_address:
        :param port:
        :return: VOID
        """
        try:
            # use the self.client to create a connection with the server
            self.clientsocket.connect((ip_address, port))
            # print connected message
            print("[" + self.id_key + " CLIENT] Connected to tracker server: " + ip_address + "/" + str(port))
            # make request to server
            self.send(self.thp.make_request(self.ip_address, self.server.app.peer_server.port, self.id_key, path, self.torrent_info_hash, self.id_key, 0, 0, 0))
            # once the client creates a successful connection, the server will send handshake to this client.
            # client is put in listening mode to retrieve data from server.
            while True:
                # handle closed pipe
                if self.clientsocket.fileno() == -1:
                    break
                # waiting for response
                while self.process():
                    continue
        except KeyboardInterrupt:
            # handle control+c
            pass
        except:
            # handle exception
            print("Failed at tracker client connecting / during active connection: ", sys.exc_info()[0])
            self.close()
            raise
        else:
            # print disconnect message
            print("[" + self.id_key + " CLIENT] Disconnected from tracker server: " + ip_address + "/" + str(port))

    def process(self):
        """
        Process received data
        :return: BOOLEAN
        """
        data = self.server.receive(self.clientsocket)
        # check for disconnected socket
        if not data:
            return None
        # if this is a HTTP response
        if re.fullmatch(b"HTTP\/(\d.\d) 200 OK\r\n\r\n.+", data):
            (interval, peers) = self.thp.parse_announce(data)
            # todo interval timed connection
            # pass peers to peer server if list is not empty
            if peers:
                for peer_info in peers:
                    # add peer to swarm if not exists
                    if not peer_info['peer_id'] in self.server.swarm:
                        self.server.add_peer_to_swarm(peer_info['peer_id'].decode('ascii'), peer_info['ip'].decode('ascii'), peer_info['port'])
        else:
            print("[" + self.id_key + " CLIENT] Unsupported message")
        return True
