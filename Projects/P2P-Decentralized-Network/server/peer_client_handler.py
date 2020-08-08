#######################################################################################
# File:             peer_client_handler.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           peer_client_handler = PeerClientHandler() # creates object
########################################################################################

import yabencode
import sys

sys.path.insert(0, './client')

from client_handler import ClientHandler
from peer_client import PeerClient


class PeerClientHandler(ClientHandler):
    def __init__(self, ready, server_instance, clientsocket, addr):
        # inherit from base class
        super().__init__(ready, server_instance, clientsocket, addr)
        # init status
        self.status = { 'choked': True, 'interested': False }

    def run(self):
        # print client connected message
        print("[" + self.server.id_key + " SERVER] Client \"" + str(self.client_id) + "\" connected.")
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
            except:
                # handle other exceptions
                print("Failed at running at client thread: ", sys.exc_info()[0])
                raise
        # remove users from server client list
        self.delete_client_data()
        # print client disconnected message
        print("[" + self.server.id_key + " SERVER] Client \"" + str(self.client_id) + "\" disconnected.")

    def process(self):
        """
        Process input
        """
        data = self.server.receive(self.clientsocket)
        # check for disconnected socket
        if not data:
            return None
        data = yabencode.decode(data)
        # if data is handshake
        if 'info_hash' in data and 'peer_id' in data and 'pstrlen' in data and 'pstr' in data:
            # parse handshake
            (info_hash, peer_id) = self.server.pwp.parse_handshake(data)
            # do nothing if torrent hash does not match
            if not self.validate_torrent_info_hash(info_hash):
                return False
            # set peer_id to id_key
            self.id_key = peer_id
            # send back after first handshake
            self.server.send(self.clientsocket, self.server.pwp.make_handshake(self.server.torrent_info_hash, self.server.id_key))
            # set connection non-blocking
            self.clientsocket.setblocking(False)
            # send choked
            # send choked
            self.server.send(self.clientsocket, self.server.pwp.make_message(self.server.pwp.TYPE_CHOKE))
            # send not not_interested
            self.server.send(self.clientsocket, self.server.pwp.make_message(self.server.pwp.TYPE_UNINTERESTED))
        # if not but it is pwp
        elif 'id' in data:
            # parse message
            message = self.server.pwp.parse_message(data)
            if data['id'] == self.server.pwp.TYPE_CHOKE:
                # set choked status to True
                self.status['choked'] = True
                print("[" + self.server.id_key + " SERVER] Set peer '" + self.id_key + "' choked.")
            elif data['id'] == self.server.pwp.TYPE_UNCHOKE:
                # set choked status to False
                self.status['choked'] = False
                print("[" + self.server.id_key + " SERVER] Set peer '" + self.id_key + "' unchoked.")
            elif data['id'] == self.server.pwp.TYPE_INTERESTED:
                # set interested status to True
                self.status['interested'] = True
                print("[" + self.server.id_key + " SERVER] Set peer '" + self.id_key + "' interested.")
            elif data['id'] == self.server.pwp.TYPE_UNINTERESTED:
                # set interested status to False
                self.status['interested'] = False
                print("[" + self.server.id_key + " SERVER] Set peer '" + self.id_key + "' uninsterested.")
            elif data['id'] == self.server.pwp.TYPE_HAVE:
                # TODO
                pass
            elif data['id'] == self.server.pwp.TYPE_BITFIELD:
                # TODO
                pass
            elif data['id'] == self.server.pwp.TYPE_REQUEST:
                # TODO
                pass
            elif data['id'] == self.server.pwp.TYPE_PIECE:
                # TODO
                pass
            elif data['id'] == self.server.pwp.TYPE_CANCEL:
                # TODO
                pass
            elif data['id'] == self.server.pwp.TYPE_PORT:
                tracker = (self.clientsocket.getpeername()[0], data['listen-port'], None)
                self.server.app.tracker_server.trackers.append(tracker)
                print("[" + self.server.id_key + " SERVER] Added tracker '" + tracker[0] + "/" + str(tracker[1]) + "' from peer '" + self.id_key + "'.")
            elif data['id'] == self.server.pwp.TYPE_TRACKER:
                # TODO
                pass
            else:
                print("[" + self.server.id_key + " SERVER] Invalid PWP ID")
        else:
            print("[" + self.server.id_key + " SERVER] Unsupported message")
        return True

    def validate_torrent_info_hash(self, peer_torrent_info_hash):
        """
        compare the info_hash generated by this peer with another info_hash sent by another peer
        this is done to make sure that both peers agree to share the same file.
        :param peer_torrent_info_hash: the info_hash from the info section of the torrent sent by other peer
        :return: True if the info_hashes are equal. Otherwise, returns false.
        """
        return self.server.torrent_info_hash == peer_torrent_info_hash
