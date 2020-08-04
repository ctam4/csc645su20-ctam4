import uuid
import hashlib
from threading import Thread
import torf
import sys

sys.path.insert(0, './server')

from peer_server import PeerServer
from tracker_server import TrackerServer

class Peer(object):
    PEER_SERVER_PORT = 6000
    TRACKER_SERVER_PORT = 7000
    # ID Constants for roles
    ROLE_PEER = 0
    ROLE_LEECHER = 1
    ROLE_SEEDER = 2

    def __init__(self, torrent_info, ip_address='127.0.0.1', peer_port=PEER_SERVER_PORT, tracker_port=TRACKER_SERVER_PORT, role=ROLE_PEER):
        # torrent info from CLI
        self.torrent_info = torrent_info
        # generate peer id (20 bytes per BitTorrent spec) with prefix and uuidv4
        self.id_key = b'-ZZ0000-'.decode() + str(uuid.uuid4()).replace('-', '')[0:12]
        # create PeerServer and TrackerServer objects
        self.tracker_server = TrackerServer(ip_address, tracker_port, self.id_key, self, self.torrent_info)
        self.peer_server = PeerServer(ip_address, peer_port, self.id_key, self, self.torrent_info)
        # default role is PEER
        self.role = role
        # empty routing table
        self.routing_table = {}

    def run_peer_server(self):
        """
        Create and run a threaded peer server
        """
        try:
            Thread(
                target=self.peer_server.run,
                args=()
                ).start()
        except KeyboardInterrupt:
            # handle control+c
            pass
        except:
            # Handle exceptions
            print("Failed at threading peer server: ", sys.exc_info()[0])
            raise

    def run_tracker_server(self):
        """
        Create and run a threaded tracker server
        """
        try:
            Thread(
                target=self.tracker_server.run,
                args=()
                ).start()
        except KeyboardInterrupt:
            # handle control+c
            pass
        except:
            # Handle exceptions
            print("Failed at threading tracker server: ", sys.exc_info()[0])
            raise

    def _add_entry_to_routing_table(self, peer_id, piece_index, block_index, block_pointer, block_flag):
        """
        adds an entry to the routing table. HINT: use the hash_info as the key in the routing table.
        NOTE: this method must be executed inside the process_block() method
        :param peer_id: the id of the peer that is sending this block
        :param piece_index: the index of the piece this block belongs. (piece index starts at 0)
        :param block_index: the block index (block index starts at 0)
        :param block_data: the block
        :param block_flag: Set to 1 bit if this is the last block to complete the piece. Otherwise, set to 0 bit
        :return: VOID
        """
        routing_table_entry = { 'hash_info': hash_info, 'peer_id': peer_id, 'piece_index': piece_index,
                               'block_index': block_index, 'block_pointer': block_pointer, 'flag': block_flag }
        self.routing_table.insert(hash_info, routing_table_entry)

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
        deletes all the blocks of a piece from the routing table
        note that this method can be only called after the piece has been validated via hash
        :param piece_index: the piece index belonging to all the blocks that must be removed from the routing table
        return: VOID
        """
        self.routing_table = { k : v for k, v in self.routing_table.items() if v['piece_index'] != piece_index }

    def is_piece_validated(piece):
        """
        TODO: validates a piece
              1. hash the piece passed as a parameter
              2. get the the piece in from the .torrent with the same index
              3. compare hashes
        :param piece the piece to be validated
        :return True if the piece is validated. Otherwise, returns false.
        """
        # hash the piece passed as a parameter
        hashed_piece = hashlib.sha1(piece)
        # @TODO get the the piece in from the .torrent with the same index

        # @TODO compare hashes
        return False


if __name__ == '__main__':
    # check command line arguments
    if len(sys.argv) == 1:
        print("Missing torrent file path")
    elif len(sys.argv) == 2:
        try:
            # read torrent file using path to torrent_info
            # sys.argv[1] is path of torrent file
            torrent_info = torf.Torrent.read(sys.argv[1])
        except torf.ReadError:
            print("Invalid torrent file path")
        except torf.MetainfoError:
            print("Invalid torrent metainfo")
        except:
            # Handle exceptions
            print("Failed at loading torrent file: ", sys.exc_info()[0])
            raise
        else:
            print("Torrent file (SHA1 " + torrent_info.infohash + ") from '" + sys.argv[1] + "' has loaded")
            # create Peer object
            peer = Peer(torrent_info)
            # start servers
            peer.run_tracker_server()
            peer.run_peer_server()
    else:
        print("Invalid arguments")
