#######################################################################################
# File:             tracker_server.py
# Author:           Calvin Tam
# Purpose:          CSC645 Assigment #2 P2P Decentralized Network with BitTorrent Protocol
# Description:      Template Server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this server class, and use a version of yours instead.
# Running:          This class is dependent of other classes.
# Usage :           tracker_server = TrackerServer() # creates object
########################################################################################

from threading import Thread, Event, Timer
import torf
import urllib.parse
import sys

sys.path.insert(0, './client')
sys.path.insert(0, './thp')

from server import Server
from tracker_client import TrackerClient
from tracker_client_handler import TrackerClientHandler
from thp import THP


class TrackerServer(Server):
    """
    TrackerServer inherits from Server with tracker functions
    """
    CLIENT_MIN_PORT_RANGE = 7001
    CLIENT_MAX_PORT_RANGE = 7010

    def __init__(self, ip_address, port, id_key, app, torrent_info):
        super().__init__(ip_address, port, id_key)
        self.app = app
        self.torrent_info = torrent_info
        self.torrent_info_hash = self.torrent_info.infohash
        self.num_pieces = self.torrent_info.pieces
        # init THP
        self.thp = THP()
        # empty swarm
        # entry format - peer_id: { peer_ip, peer_port, total_uploaded, total_downloaded, left }
        self.swarm = {}
        # empty announce trackers list
        self.trackers = []

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
        client_handler = TrackerClientHandler(ready, self, clientsocket, address)
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
        # send request to all announce if list is not empty
        if not self.trackers:
            print("[" + self.id_key + " SERVER] Empty trackers list to connect")
        else:
            try:
                print("[" + self.id_key + " SERVER] Connecting to trackers by threads")
                self.connect_all_thread(self.trackers)
            except:
                # Handle exceptions
                print("Failed at threading tracker server: ", sys.exc_info()[0])
                raise

    def run(self):
        """
        Inherit run() from base class and start parsing trackers lists from torrent file
        """
        super().run()
        # send request to all announce
        try:
            print("[" + self.id_key + " SERVER] Parsing trackers")
            for tracker_tier in self.torrent_info.trackers:
                for url in tracker_tier:
                    # split tracker address
                    parsed_url = urllib.parse.urlparse(url)
                    if parsed_url[0] == 'http':
                        tracker = (parsed_url[1].split(":")[0], int(parsed_url[1].split(":")[1]), parsed_url[2] or None)
                        # only add to trackers list if not exist
                        if not tracker in self.trackers:
                            self.trackers.append(tracker)
        except torf.URLError:
            print("Invalid tracker URLs")
            raise
        except:
            # Handle exceptions
            print("Failed at parsing trackers: ", sys.exc_info()[0])
            raise
        # make first tracker connection
        self.timed_connection()

    def connect(self, ip_address, client_port_to_bind, path):
        """
        Create a new client object and bind the port given as a parameter to that specific client.
        Then use this client to connect to the tracker (server) listening in the ip address provided as a parameter
        :param ip_address: the tracker ip address that the client needs to connect to
        :param client_port_to_bind: the port to bind to a specific client
        :param path:
        :return: VOID
        """
        try:
            # create a client object
            client = TrackerClient(self)
            # create a threaded client connecting to tracker
            Thread(
                target=client.connect,
                args=(ip_address, client_port_to_bind, path)
                ).start()
        except:
            # Handle exceptions
            print("Failed at threading tracker client: ", sys.exc_info()[0])
            raise

    def add_peer_to_swarm(self, peer_id, peer_ip, peer_port):
        """
        when a peers connects to the network adds this peer to the list of peers connected
        :param peer_id:
        :param peer_ip:
        :param peer_port:
        :return:
        """
        swarm_entry = { 'peer_ip': peer_ip, 'peer_port': peer_port, 'total_uploaded': 0, 'total_downloaded': 0, 'left': 0 }
        # insert peer_info into swarm using peer_id index
        self.swarm[peer_id] = swarm_entry
        print("[" + self.id_key + " SERVER] Peer '" + peer_id + "' added to swarm.")

    def remove_peer_from_swarm(self, peer_id):
        """
        removes a peer from the swarm when it disconnects from the network
        Note: this method needs to handle exceptions when the peer disconnected abruptly without
        notifying the network (i.e internet connection dropped...)
        :param peer_id:
        :return:
        """
        # remove peer per id
        self.swarm.pop(peer_id)
        print("[" + self.id_key + " SERVER] Peer '" + peer_id + "' removed from swarm.")

    def broadcast(self):
        """
        broadcast the list of connected peers to all the peers in the network.
        :return:
        """
        # send swarm to all connected clients
        for client_id in self.clients:
            self.send(self.clients[client_id].clientsocket, self.thp.make_announce(self.swarm))

    def update_peer_in_swarm(self, peer_id, total_uploaded, total_downloaded, left):
        """
        sets the total data uploaded, downloaded, left so far by the peer passed as a parameter
        :param peer_id:
        :return: VOID
        """
        # check peer_id exists in swarm
        swarm_entry = self.swarm.get(peer_id)
        if not swarm_entry:
            return False
        # update values and set back to swarm
        swarm_entry['total_uploaded'] = total_uploaded
        swarm_entry['total_downloaded'] = total_downloaded
        swarm_entry['left'] = left
        self.swarm[peer_id] = swarm_entry
        return True
