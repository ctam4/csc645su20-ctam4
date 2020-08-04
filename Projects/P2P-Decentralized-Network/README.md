# P2P Decentralized Network with BitTorrent Protocol

Please use this README file to provide the following documentation for this project:

* Your name and student id
  - Calvin Tam (917902523)
* General description of the project (a few sentences)
  - A BitTorrent client with DHT. (THP for trackers, PWP for peers)
* If you used external Python modules/libraries. Provide a requirements.txt file  
* Python version and compatibility issues (if any)
  - 3.7.3
* Clear and specific instructions about how to run your project. If your project does not run or contains errors, you'll get a 0 in the project no matter how much work you put on it. So, test your code properly and make sure that it runs without errors.
  - Use `age2.torrent`. `age.torrent`'s announce list is missing protocol and gives error on importing with external library.
  - Run this command to start: `python3 peer.py <torrent file path>`
* A few sentences about all the challenges you found during the implementation of this project and how you overcame them. Please be honest here. 
  - No idea how the protocol works e.g. diagrams. PDF provided helps a little bit but not much. I had to google and check specificiation online for implementation. At this point, I have no idea which message goes after another message. There should be at least a protocol flow diagram or some output example.
  - Time limitation in summer. This project requires the labs files to begin but there are too many blanks. I do not even know if the labs are working correctly.
  - Handling bencode data for THP and PWP is complicated. I am using `yabencode` library just to decode/encode data for simplifiction. There is no point to manually parsing binary while this is not the logic part of the protocol.
  - Manually coding and parasing THP (HTTP based protocol) makes it complicated and difficult from scratch while we are not allowed to use any library for basic HTTP server.
  - If the goal is to exchange data using BitTorrent protocols, then this project is way too advanced from scartch. TCP project should be making a tracker server instead. I can only reuse some core part of code from TCP project as most codes are useless in this proejct.

## Note that failure to provide the above docs will result in a 30% deduction in your final grade for this project. 

# Project Guidelines 

In this project, and using the knowledge gathered in the labs, you will build a decentralized P2P network using the BitTorrent Protocol. Recall that in a decentralized P2P network the peer is the client, server and tracker at the same time.

## Peer 

The peer class is the main class of this network. It must to have the following functionalities:

### Server Side 

  * Handling multiple peers connections at the same time

  * Uploading data to the swarm, so other peers can download that data 

  * Implementing tracker services: the server side of a peer, when connected by other peer for the first time, needs to update the list of ip addresses connected to the network, and broadcast it to all the peers in the network. 
  
### Client side 

  * Connect to other peers to download data from them ( connect to their server side )
  
  * Handeling clients running in different ports in the same machine 
  
  * Routing data 
  
### General 

  * Changing status ( i.e from peer to seeder ), and therefore, changing services provided. 
  
  * Being able to understand the Peer Wire Protocol which is in charge of handling the communication and messages sent between peers 
  
  * Implementing scalability: being able to be connected to multiple swarms sharing multiple files at the same time. 
  
  * Persistency: if the peers is disconnected from the network, and then it reconnects, the data and its configuration in the network must be persistent. (i.e restarting the downloading process in the same point where it was left before desconnecting)
  
  * For testing purposes, each peer must be run in a different machine in the same Local Area Network (LAN)
  
# Grading Guidelines 

1. If your peer file does not run, you´ll get a zero in this project. 

2. Provide correct and complete documentation. Make sure to specify in your docs how to run your program and the Python version you used to implement it. 

3. Your project will be graded based on completeness and correctness. For each services that is not implemented, you´ll get points deducted. 

4. No template is provided in this project since you can reuse the client, server and peer classes from labs and other projects

# General Implementation Guidelines 

Note this are only high level guidelines. Your implementation will need to take into consideration more specific details to meet the minimum functionality/requirements in this app. 

1. Download the age.txt file and age.torrent file from ilearn 
2. Change the announce value of your age.torrent to the ip address of the machine where your first seeder will be run. 
3. Put the age.torrent file in the torrents folder of the project in all the machines you run a peer. 
4. Run your first peer: your first peer in the network is the announce and the first seeder in the network, then run the server and the tracker of this peer and finally wait for other peer connections. Once a peer connects, the server accepts the peer (if not chocked and the peer is interested) and then pass the request to the tracker. The tracker will add this peer to the list of peers connected to the network and then will broadcast this updated list to all the peers connected in the network. Note the seeder is just uploading data in this swarm. It does not download any data. However, a seeder may be a seeder in swarm X and a peer in swarm Y. Think about this because this concept is important......
5. Run the next peer in a different machine. This peer should scan the age.torrent file, extract the announce ip address, name of the file (age.txt) and check that this ip address is not the same as the one this peer is using, then, it should go the the shareable folder and check if it has the file age,txt. If the file is there, then this peer should automatically set its status to seeder. Otherwise, the status is kept as peer. In any of both cases, this peer connects to the announcer to get the list of ip_addresses connected to the network. If seeder, the seeder just run the server and the tracker and wait there for connections. If peer, then do step 6. 
6. If peer, (not seeder nor announce) then it must connect to all the peers in the network running a client socket per connection. 
7. When a peer connects to another peer, after the initial handshake, the peer trying to connect sends to the other peer if it is interested or not, then the other peers send back a response with choked or non-choked, if not chocked then this peer sends its bitfield, the other peer will see which blocks are missing, and will wait for a request from this peer. Once this peer sends a requests asking for a block, the sharing process begins. 
8. When a peer gets the the last block of a piece, then it will go to the routing table and will extract from there all the blocks belonging to that piece, then it will create a copy of the original piece, hash the copy of the original piece, and will compare it to the one found in the torrent file that match the piece index. If both pieces are the same then the piece is validated, and all the blocks from that piece in the routing table must be deleted. 
9. Once the hash of a piece is validated, its original piece needs to be added to the temporal age.txt file in the exact byte offset that it belongs. Note that pieces may be downloaded in random order and therefore the tmp age.txt file must have the same length as the original file even if the tmp file is empty. 
10. When a peer has all the pieces of the file, it moves the complete tmp file to the shareable folder and then change its status to seeder. 

# The Tit-For-Tat Protocol

In this assignment, peers and seeders are implementing the tit-for-tat protocol. Each seeder or peer can uplload data to a maximum of four peers. When a seeder is uploading to four peers, it change its status to choked. A peer downloading data, can download data only from a maximum of four peers or seeders. This situation needs to be revaluated every 30 seconds because the network want to give oportunities to the rarest peers. In addition, this is also based on the temporal downloads and uploads rates of each peer. 

See P2P.pdf for more info about how to compute temporal upload and downloads rates. 

# HTPBS for Showing Pieces Downloading/Uploading Progresses 

In order to show the progress of the pieces your peer is uploading or downloading to/from the P2P network, you can use the htpbs (horizontal threaded progress bars) library. This library tracks the progress of threaded jobs and is costomizable to for your project. Exactelly what you need for this project!. For more info about this library: https://pypi.org/project/htpbs/

### Install with PIP

```python 
pip3 install htpbs
```

# Submission Guidelines 

This project is due the last day of the semester. After you complete and test your project, go to the assignments table, located in main README file, and set this project to "done". Projects that are not set to "done" in the table of assignments won't be graded because I will assume that they haven't been completed. No exceptions here!!!. 
  
  
 


    


