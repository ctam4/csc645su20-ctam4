import math
from bitarray import bitarray # you must install this library


class PWPMessage:
    """
    This class represents a basic implementation of the Peer Wire Protocol (PWP) used by BitTorrent protocol
    to provide reliable communication methods between peers in the same P2P network
    USAGE:
        message = Message()
        message.init_bitfield()
    """
    # constants
    X_BITFIELD_LENGTH = b'0000'
    X_PIECE_LENGTH = b'0000'

    def __init__(self):
        # A keep-alive message must be sent to maintain the connection alive if no command
        # have been sent for a given amount of time. This amount of time is generally two minutes.
        self.keep_alive = {'len': b'0000'}
        # The uploader cannot upload more data to the swarm. Causes could be congestion control..
        self.choke = {'len': b'0001', 'id': 0}
        # The uploader is ready to upload more data to the swarm.
        self.unchoke = {'len': b'0001', 'id': 1}
        # The downloader is interested in downloading data from the requested peer.
        self.interested = {'len': b'0001', 'id': 2}
        # The downloader is not interested in downloading data from the requested peer.
        self.not_interested = {'len': b'0001', 'id': 3}
        # The payload is a piece that has been successfully downloaded and verified via the hash.
        self.have = {'len': b'0005', 'id': 4, 'piece_index': None}
        # The payload is a bitfield representing the pieces that have been successfully downloaded.
        # The high bit in the first byte corresponds to piece index 0.
        # Bits that are cleared indicated a missing piece, and set bits indicate a valid and available piece.
        # Spare bits at the end are set to zero.
        # [[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
        self._bitfield = {'len': b'0013' + self.X_BITFIELD_LENGTH, 'id': 5, 'bitfield': []}
        # The request message is fixed length, and is used to request a block.
        # The payload contains the following information:
        #     index: integer specifying the zero-based piece index
        #     begin: integer specifying the zero-based byte offset within the piece
        #     length: integer specifying the requested length.
        self.request = {'len': b'0013', 'id': 6, 'index': None, 'begin': None, 'length': None}
        # The piece message is variable length, where X is the length of the block.
        # The payload contains the following information:
        #     index: integer specifying the zero-based piece index
        #     begin: integer specifying the zero-based byte offset within the piece
        #     block: block of data, which is a subset of the piece specified by index.
        self.piece = {'len': b'0009' + self.X_PIECE_LENGTH, 'id': 7, 'index': None, 'begin': None, 'block': None}
        # The payload is identical to that of the "request" message. It is typically used during "End Game"
        # The "End Game"
        self.cancel = {'len': b'0013', 'id': 8, 'index': None, 'begin': None, 'length': None}
        # The port message is sent by newer versions of the Mainline that implements a DHT tracker.
        # The listen port is the port this peer's DHT node is listening on.
        # This peer should be inserted in the local routing table (if DHT tracker is supported).
        self.port = {'len': b'0003', 'id': 9, 'listen-port': None}
        #  Tracker requests have the following keys:
        #      info_hash
        #            The 20 byte sha1 hash of the bencoded form of the info value from the metainfo file.
        #            This value will almost certainly have to be escaped.
        #            Note that this is a substring of the metainfo file. The info-hash must be the hash of the encoded
        #            form as found in the .torrent file, which is identical to bdecoding the metainfo file, extracting
        #            the info dictionary and encoding it if and only if the bdecoder fully validated the input
        #            (e.g. key ordering, absence of leading zeros). Conversely that
        #            means clients must either reject invalid metainfo files or extract the substring directly.
        #            They must not perform a decode-encode roundtrip on invalid data.
        #      peer_id
        #            A string of length 20 which this downloader uses as its id. Each downloader generates its own id at
        #            random at the start of a new download. This value will also almost certainly have to be escaped.
        #      ip
        #            An optional parameter giving the IP (or dns name) which this peer is at. Generally used for the
        #            origin if it's on the same machine as the tracker.
        #      port
        #            The port number this peer is listening on. Common behavior is for a downloader to try to listen
        #            on port 6881 and if that port is taken try 6882, then 6883, etc. and give up after 6889.
        #      uploaded
        #            The total amount uploaded so far, encoded in base ten ascii.
        #      downloaded
        #            The total amount downloaded so far, encoded in base ten ascii.
        #      left
        #            The number of bytes this peer still has to download, encoded in base ten ascii. Note that this
        #            can't be computed from downloaded and the file length since it might be a resume, and there's a
        #            chance that some of the downloaded data failed an integrity check and had to be re-downloaded.
        #      event
        #            This is an optional key which maps to started, completed, or stopped (or empty, which is the
        #            same as not being present). If not present, this is one of the announcements done at regular
        #            intervals. An announcement using started is sent when a download first begins, and one using
        #            completed is sent when the download is complete. No completed is sent if the file was complete
        #            when started. Downloaders send an announcement using stopped when they cease downloading.
        self.tracker = {'torrent_info_hash': -1, 'peer_id': -1, "ip": -1, 'port': -1, 'uploaded': -1,
                        'downloaded': -1, 'left': -1, 'event': -1}

    #############################  Bitfield Methods ####################################################

    def init_bitfield(self, num_pieces):
        """
        Initializes the bitfield with all the pieces set to missing: b'00000000'
        NOTE: Initialization of the bitarry must be in bytes. You can use the
        library bitarray to create pieces like this: bitarray(8)
        :param num_pieces: the number of pieces defined in the .torrent file
        :return: Void
        """
        size_bitfield = int(math.ceil(num_pieces / 8))
        spare_bits = (8 * size_bitfield) - num_pieces
        for i in range(size_bitfield - 1):
            # create a bitarray (piece) of 8 bits size
            piece_bitfield = bitarray(8)
            # set all the bits to 0 (missing piece)
            piece_bitfield.setall(0)
            # add the new piece to the bitfield (self._bitfield['bitfield])
            self._bitfield['bitfield'].append(piece_bitfield)
        # create a new bitarray (piece) of spare bits size
        spare_piece_bitfield = bitarray(spare_bits)
        # # set all the bits to 0 (missing piece)
        spare_piece_bitfield.setall(0)
        # add the new piece to the bitfield (self._bitfield['bitfield])
        self._bitfield['bitfield'].append(spare_piece_bitfield)

    def get_bitfield(self):
        """
        get the bitfield payload
        :return: the bitfield payload
        """
        return self._bitfield

    def get_bitfield_piece(self, piece_index):
        """
        gets a piece from the bitfield
        :param piece_index:
        :return: the piece bitfield located at index 'piece_index'
        """
        return self._bitfield['bitfield'][piece_index]

    def get_bitfield_block(self, piece_index, block_index):
        """
        gets a block from the bitfield
        :param piece_index:
        :param block_index:
        :return: the block bit located at index 'block_index'
        """
        return self._bitfield['bitfield'][piece_index][block_index]

    def is_block_missing(self, piece_index, block_index):
        """
        determines if a block is missing (missing blocks are set to bit 0)
        :param piece_index:
        :param block_index:
        :return: True if the block is missing. Otherwise, returns False
        """
        return not self._bitfield['bitfield'][piece_index][block_index]

    def is_piece_missing(self, piece_index):
        """
        determines if a piece is missing (missing pieces has at least one block set to bit 0)
        :param piece_index:
        :return: True if the piece is missing. Otherwise, returns False
        """
        piece = self._bitfield['bitfield'][piece_index]
        for block_index in range(len(piece)):
            if self.is_block_missing(piece_index, block_index):
                return True
        return False

    def next_missing_block(self, piece_index):
        """
        finds the next missing block
        :param piece_index:
        :return: the next missing block index
        """
        piece = self._bitfield['bitfield'][piece_index]
        for block_index in range(len(piece)):
            if self.is_block_missing(piece_index, block_index):
                return block_index
        return -1

    def next_missing_piece(self):
        """
        finds the next missing piece
        :return: the next missing piece index
        """
        for piece_index in range(len(self._bitfield['bitfield'])):
            if self.is_piece_missing(piece_index):
                return piece_index
        return -1

    def set_block_to_completed(self, piece_index, block_index):
        """
        set the block represented by the piece_index and block_index to b'1' or True
        :param piece_index:
        :param block_index:
        :return: VOID
        """
        self._bitfield['bitfield'][piece_index][block_index] = True