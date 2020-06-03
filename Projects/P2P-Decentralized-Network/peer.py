from client import Client
from server import Server

class Peer():
    
    SEEDER = 2;
    LEECHER = 1;
    PEER = 0;
    
    def __init__(self):
        self.role = PEER # default role
        pass
    
    # your peer inplementation here. 
    # You may rehuse the code from your labs here as help for your final implementation of this class.
