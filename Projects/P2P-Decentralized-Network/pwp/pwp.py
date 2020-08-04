import yabencode

from pwp_message import PWPMessage


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
    TYPE_PORT = 9
    TYPE_TRACKER = 10

    def __init__(self, num_pieces):
        """
        Empty constructor
        """
        self.message = PWPMessage()
        self.message.init_bitfield(num_pieces)

    def parse_handshake(self, data):
        """
        parse handshake
        :param data: binary string
        :return: TUPLE
        """
        return (data['info_hash'].decode('ascii'), data['peer_id'].decode('ascii'))

    def make_handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        implement the handshake
        :param options:
        :return: the handshake message
        """
        handshake = {'info_hash': info_hash, 'peer_id': peer_id, 'pstrlen': pstrlen, 'pstr': pstr}
        try:
            return yabencode.encode(handshake)
        except yabencode.MalformedBencodeException:
            # handle yabencode exceptions
            print("Failed to bencode data: ", sys.exc_info()[0])
            raise

    def parse_message(self, data):
        """
        parse message
        :param data: binary string
        :return: TUPLE
        """
        message = {}
        for key, value in data.items():
            if not key in ['id', 'len']:
                message[key] = value
        print(message)
        return message

    def make_message(self, message_id, payload=None):
        """
        implement the message
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
            self.TYPE_PORT: { **self.message.port, **payload },
            self.TYPE_TRACKER: { **self.message.tracker, **payload },
        }
        try:
            return yabencode.encode(switcher.get(message_id))
        except yabencode.MalformedBencodeException:
            # handle yabencode exceptions
            print("Failed to bencode data: ", sys.exc_info()[0])
            raise
