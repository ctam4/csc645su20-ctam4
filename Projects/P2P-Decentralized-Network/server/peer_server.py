from threading import Thread, Event, Timer
import torf
import sys

sys.path.insert(0, './client')
sys.path.insert(0, './pwp')

from server import Server
from peer_client import PeerClient
from peer_client_handler import PeerClientHandler
from pwp import PWP


class PeerServer(Server):
    """
    PeerServer inherits from Server with tracker functions
    """
    CLIENT_MIN_PORT_RANGE = 6001
    CLIENT_MAX_PORT_RANGE = 6010

    def __init__(self, ip_address, port, id_key, app, torrent_info):
        super().__init__(ip_address, port, id_key)
        self.app = app
        self.torrent_info = torrent_info
        self.torrent_info_hash = self.torrent_info.infohash
        self.num_pieces = self.torrent_info.pieces
        # init PWP
        self.pwp = PWP(self.num_pieces)
        # empty peers list
        self.peers = []

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new TrackerClientHandler object
        See also TrackerClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        # threading event
        ready = Event()
        # create a new client handler object and return it
        # inits all the components in client handler object
        # self is the server instance
        client_handler = PeerClientHandler(ready, self, clientsocket, address)
        # adds the client handler object to the list of all the clients objects created by this server.
        # key: client id, value: client handler
        # assumes dict was initialized in class constructor
        self.clients[client_handler.client_id] = client_handler
        # start client handler engine when it is ready
        ready.wait()
        client_handler.run()
        return client_handler

    def timed_connection(self, time=None):
        # if time is given, run on every time
        if time:
            Timer(time, self.timed_connection).start()
        # fetch peers from tracker if not empty
        if self.app.tracker_server.swarm:
            for peer_id, peer_info in self.app.tracker_server.swarm.items():
                # add peer to peers list if not exists
                if not peer_id in self.peers:
                    peer = (peer_info['peer_ip'], peer_info['peer_port'], None)
                    # only add to peers list if not exist
                    if not peer in self.peers:
                        self.peers.append(peer)
        # send request to all peers if list is not empty
        if not self.peers:
            print("[" + self.id_key + " SERVER] Empty peers list to connect")
        else:
            try:
                print("[" + self.id_key + " SERVER] Connecting to peers by threads")
                self.connect_all_thread(self.peers)
            except:
                # Handle exceptions
                print("Failed at threading peer server: ", sys.exc_info()[0])
                raise

    def run(self):
        """
        Inherit run() from base class and start connecting to peers
        """
        super().run()
        # make first tracker connection
        self.timed_connection(1)

    def connect(self, ip_address, client_port_to_bind, path):
        """
        Create a new client object and bind the port given as a parameter to that specific client.
        Then use this client to connect to the peer (server) listening in the ip address provided as a parameter
        :param ip_address: the tracker ip address that the client needs to connect to
        :param client_port_to_bind: the port to bind to a specific client
        :param path:
        :return: VOID
        """
        try:
            # create a client object
            client = PeerClient(self)
            # create a threaded client connecting to peer
            Thread(
                target=client.connect,
                args=(ip_address, client_port_to_bind, path)
                ).start()
        except:
            # Handle exceptions
            print("Failed at threading peer client: ", sys.exc_info()[0])
            raise
