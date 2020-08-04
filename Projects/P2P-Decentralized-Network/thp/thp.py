import yabencode
import re
import sys


class THP(object):
    def __init__(self):
        pass

    def parse_request(self, data):
        """
        Parse HTTP GET request
        :param data: binary string
        :return: TUPLE
        """
        # split data by line break
        request = data.split(b"\r\n")
        # split path's query into key=value
        for query in request[0].split(b" ")[1][2:].split(b"&"):
            if re.match(b"info_hash", query):
                info_hash = query.split(b"=")[1].decode('ascii')
            elif re.match(b"peer_id", query):
                peer_id = query.split(b"=")[1].decode('ascii')
            elif re.match(b"uploaded", query):
                uploaded = query.split(b"=")[1].decode('ascii')
            elif re.match(b"downloaded", query):
                downloaded = query.split(b"=")[1].decode('ascii')
            elif re.match(b"left", query):
                left = query.split(b"=")[1].decode('ascii')
        # parse 'Host' for peer_ip and perr_port
        for query in request[1:]:
            if re.match(b"Host", query):
                url = query[6:].split(b":")
                peer_ip = url[0].decode('ascii')
                peer_port = int(url[1].decode('ascii'))
        return (info_hash, peer_id, uploaded, downloaded, left, peer_ip, peer_port)

    def make_request(self, ip_address, port, id_key, tracker_path, info_hash, peer_id, uploaded, downloaded, left):
        """
        Make HTTP GET request to tracker
        :return: BINARY STRING
        """
        # return None for invalid parameter
        if uploaded < 0 or downloaded < 0 or left < 0:
            return None
        request = b"GET "
        if not tracker_path:
            tracker_path = "/"
        request += tracker_path.encode('ascii')
        request += b"?info_hash=" + info_hash.encode('ascii')
        request += b"&peer_id=" + peer_id.encode('ascii')
        request += b"&uploaded=" + str(uploaded).encode('ascii')
        request += b"&downloaded=" + str(downloaded).encode('ascii')
        request += b"&left=" + str(left).encode('ascii')
        request += b" HTTP/1.1\r\n"
        request += b"Host: " + ip_address.encode('ascii') + b":" + str(port).encode('ascii') + b"\r\n"
        request += b"User-Agent: " + id_key.encode('ascii') + b"\r\n"
        request += b"Accept-Encoding: gzip\r\n"
        request += b"Connection: Close"
        return request

    def parse_announce(self, data):
        """
        Parse HTTP response
        :param data: binary string
        :return: TUPLE
        """
        # split data by line break
        response = data.split(b"\r\n")
        # decode announce dict
        announce = yabencode.decode(response[2])
        return (announce['interval'], announce['peers'])

    def make_announce(self, swarm):
        """
        Announce peers
        :param swarm:
        :return: DICT
        """
        # make a peers list of dict per spec
        peers = []
        for peer_id, peer in swarm.items():
            peer_info = { 'peer_id': peer_id, 'ip': peer['peer_ip'], 'port': peer['peer_port'] }
            peers.append(peer_info)
        # make an announce dict
        announce = { 'interval': 0, 'peers': peers }
        response = b"HTTP/1.1 200 OK\r\n\r\n"
        try:
            response += yabencode.encode(announce)
        except yabencode.MalformedBencodeException:
            # handle yabencode exceptions
            print("Failed to bencode data: ", sys.exc_info()[0])
            raise
        return response
