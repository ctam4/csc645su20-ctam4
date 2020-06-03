# LAB 9: P2P Routing Table
In this lab, students will learn about the handling and routing concepts in a P2P network and why they are so important.
In lab 8, students learned about the challenges found while implementing downloading mechanises to download data from 
other peers. Two of the main challenges found when downloading data from other peers are the routing 
processes of that data 

## Routing Blocks 

Routing blocks is the process of routing pieces of data coming from different peers to the file they belong. 
This is a difficult process because those pieces of data may come from different swarms. 
For example, P1, P2 and P3 are connected and sharing data in different swarms. When P1 receives a block 
(i.e block_index = 1, piece_index = 3) from P2, and at the same time, P1 is receiving (block_index = 1, piece_index = 3)
from a different swarm (different file). It needs a way of knowing to which file that block of data belongs. 
The routing process is the one that perform this task. 

One way of implementing routing in P2P is to keep track of all the blocks that are being downloaded. So, for each block 
that is downloaded from a peer, the block is added to a routing table. The routing table entry contains the following 
columns or keys:

```python
routing_table_entry = {'hash_info': hash_info, 'peer_id': 0, 'piece_index': 0,
                               'block_index': 0,  'block_pointer': block_pointer, 'flag': block_flag} 
```

#### Hash Info

The hash info of the file that is being shared. This info can be extracted from the tracker. 

#### Peer ID 

The peer id representing the peer that sent the data. 

#### Piece and Block Indexes 

The piece and the block indexes of the data that represent the data that is retrieved

#### Block Pointer

The pointer pointing to the tmp file in disk that contain the block. Note blocks pointers are developer implemented. 
In other words, the developer decides how to implement the pointer.  

#### The Block Flag

This process similar to datagram fragmentation (frag_flag field ) in the data plane of the network layer. So, the flag 
is set to bit 0 for all the blocks from the same piece but the last one which flag is set to 1. 

Take into account that since a block, by itself, cannot be validated and only complete pieces can be validated, then 
blocks must be kept in disk until the piece is completed. We keep track of this blocks using the routing table. 

The following is a logical example of how a routing table is represented in memory:

```python 
| hash_info | peer_id | piece_index | block_index |  block_pointer | block_flag |
---------------------------------------------------------------------------------
| 34hg56h4h | 48uhg7  |      12     |     7       |     wh2774h    |    0       |
| 34hg56h4h | 45jhyr  |      10     |     6       |     hdhdyfg    |    0       |
| 34hg56h4h | 38hhtg  |      10     |     0       |     dhehdhe    |    0       |
| 34hg56h4h | 7gghft  |      12     |     3       |     wh3hbdh    |    0       |
| 37hghhtbb | 3hhdgy  |      12     |     3       |     2heh4hh    |    0       |
```

## Your job in this lab 

1. Copy and paste (or add) the server.py and client.py from your TCP Client-Server assignment into this lab folder
2. Copy and paste your tracker.py implemented in lab 8 into this lab folder
3. Copy and paste all the methods implemented in lab 8 (peer.py) into the peer.py file in this lab. Do, it in the proper
place so you do not delete the actual methods that need to be implemented in this lab.
2. Implement all the methods marked with TODO in the peer.py file from this lab

### Testing 

1. Run three different peers in different machines (or the same machine. Be careful with server and client ports) 
2. Print routing table for each block you add to the table. 


 








