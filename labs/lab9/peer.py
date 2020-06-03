"""
Lab 9: Routing and Handing
Implement the routing and handling functions
Note: Include in this Peer class all the implemented methods from Peer class in lab 8.
"""
from server import Server # assumes server.py is in this directory.
from client import Client # assumes client.py is in this directory.
from tracker import Tracker # assumes tracker.py is this directory.

class Peer ():

    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010

    def __init__(self, server_ip_address):
        self.routing_table = {} # empty routing table
    
    
    # Your code from peer.py in lab 8 can be added here.

    def _add_entry_to_routing_table(self, peer_id, piece_index, block_index, block_pointer, block_flag):
        """
        TODO: adds an entry to the routing table. HINT: use the hash_info as the key in the routing table.
        TODO: NOTE: this method must be executed inside the process_block() method
        :param peer_id: the id of the peer that is sending this block
        :param piece_index: the index of the piece this block belongs. (piece index starts at 0)
        :param block_index: the block index (block index starts at 0)
        :param block_data: the block
        :param block_flag: Set to 1 bit if this is the last block to complete the piece. Otherwise, set to 0 bit
        :return: VOID
        """
        routing_table_entry = {'hash_info': hash_info, 'peer_id': peer_id, 'piece_index': piece_index,
                               'block_index': block_index, 'block_pointer': block_pointer, 'flag': block_flag}

        pass  # your code here
        
    def process_block(self, peer_id, piece_message):
        """
        TODO: takes the piece message sent by another peer (self.piece from message.py) and extracts all its data
        TODO: if the block is not the last block of the piece, then save the block data in a tmp file in disk,
              and create a pointer to that file. To optimize this process, you should keep your blocks data organized
              in the same file using a custom criteria (i.e blocks from the same hash_info file)
        TODO: using the data extracted from the piece message, and the pointer to the block data, add the entry to the routing table.

        :param peer_id: the peer id that sent the message
        :param piece_message: the self.piece message containing the payload representing the block data
        :return: VOID
        """
        return 0 # return the block
    
    def remove_piece_from_routing_table(piece_index):
        """
        TODO: deletes all the blocks of a piece from the routing table
              note that this method can be only called after the piece has
              been validated via hash
        :param piece_index: the piece index belonging to all the blocks that must be removed from the routing table
        return: VOID
        """
        pass # your code here 
    
    def is_piece_validated(piece):
        """
        TODO: validates a piece
              1. hash the piece passed as a parameter
              2. get the the piece in from the .torrent with the same index
              3. compare hashes
        :param piece the piece to be validated
        :return True if the piece is validated. Otherwise, returns false. 
        """
        return False # your code here
        

