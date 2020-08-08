#######################################################################################
# File:             peer_client.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template Client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           peer_client = PeerClient() # creates object
########################################################################################

import socket
import pickle
import yabencode
import sys

sys.path.insert(0, './pwp')

from client import Client
from pwp import PWP


class PeerClient(Client):
    def __init__(self, server):
        """
        Inhert __init__ from base class and process new parameter
        :param server:
        :param torrent_info_hash:
        :return: VOID
        """
        super().__init__(server)
        self.torrent_info_hash = self.server.torrent_info_hash
        # init PWP
        self.pwp = PWP(self.server.num_pieces)
        # init status
        self.status = { 'choked': True, 'interested': False }

    def connect(self, ip_address, port, path=None):
        """
        Connects to a server. Implements exception handler if connection is resetted.
	    Then retrieves the cliend id assigned from server, and sets
        :param path:
        :return: VOID
        """
        try:
            # use the self.client to create a connection with the server
            self.clientsocket.connect((ip_address, port))
            # print connected message
            print("[" + self.server.id_key + " CLIENT] Connected to peer server: " + ip_address + "/" + str(port))
            # send handshake
            self.send(self.pwp.make_handshake(self.torrent_info_hash, self.server.id_key))
            # once the client creates a successful connection, the server will send handshake to this client.
            # client is put in listening mode to retrieve data from server.
            while True:
                try:
                    # handle closed pipe
                    if self.clientsocket.fileno() == -1:
                        break
                    # waiting for response
                    while self.process():
                        continue
                except BrokenPipeError:
                    # handle broken pipe
                    pass
                except BlockingIOError:
                    # handle non blocking empty pipe
                    pass
        except KeyboardInterrupt:
            # handle control+c
            pass
        except:
            # handle exception
            print("Failed at peer client connecting / during active connection: ", sys.exc_info()[0])
            self.close()
            raise
        else:
            # print disconnect message
            print("[" + self.server.id_key + " CLIENT] Disconnected from peer server: " + ip_address + "/" + str(port))

    def process(self):
        """
        Process received data
        :return: BOOLEAN
        """
        data = self.server.receive(self.clientsocket)
        # check for disconnected socket
        if not data:
            return None
        # decode data with yabencode
        data = yabencode.decode(data)
        # if data is handshake
        if 'info_hash' in data and 'peer_id' in data and 'pstrlen' in data and 'pstr' in data:
            # parse handshake
            (info_hash, peer_id) = self.pwp.parse_handshake(data)
            # do nothing if torrent hash does not match
            if not self.validate_torrent_info_hash(info_hash):
                return False
            # set peer_id to id_key
            self.id_key = peer_id
            # send back port after first handshake
            payload = { 'listen-port': self.server.app.tracker_server.port }
            self.server.send(self.clientsocket, self.pwp.make_message(self.pwp.TYPE_PORT, payload))
            # set connection non-blocking
            self.clientsocket.setblocking(False)
            # send choked
            self.server.send(self.clientsocket, self.pwp.make_message(self.pwp.TYPE_CHOKE))
            # send not not_interested
            self.server.send(self.clientsocket, self.pwp.make_message(self.pwp.TYPE_UNINTERESTED))
        # if not but it is pwp
        elif 'id' in data:
            # parse message
            message = self.pwp.parse_message(data)
            if data['id'] == self.pwp.TYPE_CHOKE:
                # set choked status to True
                self.status['choked'] = True
                print("[" + self.server.id_key + " CLIENT] Set peer '" + self.id_key + "' choked.")
            elif data['id'] == self.pwp.TYPE_UNCHOKE:
                # set choked status to False
                self.status['choked'] = False
                print("[" + self.server.id_key + " CLIENT] Set peer '" + self.id_key + "' unchoked.")
            elif data['id'] == self.pwp.TYPE_INTERESTED:
                # set interested status to True
                self.status['interested'] = True
                print("[" + self.server.id_key + " CLIENT] Set peer '" + self.id_key + "' interested.")
            elif data['id'] == self.pwp.TYPE_UNINTERESTED:
                # set interested status to False
                self.status['interested'] = False
                print("[" + self.server.id_key + " CLIENT] Set peer '" + self.id_key + "' uninsterested.")
            elif data['id'] == self.pwp.TYPE_HAVE:
                # TODO
                pass
            elif data['id'] == self.pwp.TYPE_BITFIELD:
                # TODO
                pass
            elif data['id'] == self.pwp.TYPE_REQUEST:
                # TODO
                pass
            elif data['id'] == self.pwp.TYPE_PIECE:
                # TODO
                pass
            elif data['id'] == self.pwp.TYPE_CANCEL:
                # TODO
                pass
            else:
                print("[" + self.server.id_key + " CLIENT] Invalid PWP ID")
        else:
            print("[" + self.server.id_key + " CLIENT] Unsupported message")
        return True

    def validate_torrent_info_hash(self, peer_torrent_info_hash):
        """
        compare the info_hash generated by this peer with another info_hash sent by another peer
        this is done to make sure that both peers agree to share the same file.
        :param peer_torrent_info_hash: the info_hash from the info section of the torrent sent by other peer
        :return: True if the info_hashes are equal. Otherwise, returns false.
        """
        return self.server.torrent_info_hash == peer_torrent_info_hash
