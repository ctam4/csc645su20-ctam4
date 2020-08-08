########################################################################################################################
# Class: Computer Networks
# Date: 07/21/2020
# Lab7: P2P: The BitTorrent Peer Wire Protocol
# Goal: create a Python class that implements the services provided by the Peer Wire Protocol
# Student Name: Calvin Tam
# Student ID: 917902523
# Student Github Username: ctam4
# Instructions: Read each problem carefully, and implement them correctly.  No partial credit will be given.
########################################################################################################################

"""
Lab 7: Peer Wire Protocol (PWP)
Create a class with the basic implementation for the bitTorrent peer wire protocol
A basic template structure is provided, but you may need to implement more methods
For example, the payload method depending of the option selected
"""

from message import Message

class PWP(object):
    # pstr and pstrlen constants used by the handshake process
    PSTR = "BitTorrent protocol"
    PSTRLEN = 19
    # Define ID constants for all the message fields such as unchoked, interested....
    TYPE_CHOKE = 0
    TYPE_UNCHOKE = 1
    TYPE_INTERESTED = 2
    TYPE_UNINTERESTED = 3
    TYPE_HAVE = 4
    TYPE_BITFIELD = 5
    TYPE_REQUEST = 6
    TYPE_PIECE = 7
    TYPE_CANCEL = 8

    def __init__(self, num_pieces):
        """
        Empty constructor
        """
        self.message = Message()
        self.message.init_bitfield(num_pieces)

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        implement the handshake
        :param options:
        :return: the handshake message
        """
        handshake = {'info_hash': info_hash, 'peer_id': peer_id, 'pstrlen': pstrlen, 'pstr': pstr}
        return handshake

    def message(self, len, message_id, payload={}):
        """
        implement the message
        :param len:
        :param message_id:
        :param payload:
        :return: the message
        """
        switcher = {
            None: self.message.keep_alive,
            self.TYPE_CHOKE: self.message.choke,
            self.TYPE_UNCHOKE: self.message.unchoke,
            self.TYPE_INTERESTED: self.message.interested,
            self.TYPE_UNINTERESTED: self.message.not_interested,
            self.TYPE_HAVE: { **self.message.have, **payload },
            self.TYPE_BITFIELD: self.message.get_bitfield(),
            self.TYPE_REQUEST: { **self.message.request, **payload },
            self.TYPE_PIECE: { **self.message.piece, **payload },
            self.TYPE_CANCEL: { **self.message.cancel, **payload },
        }
        return switcher.get(message_id)


