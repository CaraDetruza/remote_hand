import socket
import network
import ubinascii
import time
import random
from common.misc import SERVER_PORT, THUMB_ID, INDEX_ID, MIDDL_ID, RINGF_ID, \
PINKY_ID, PAYLOAD_LEN, HANDSHAKE
import sys
import struct
import gc

class UDPClient:
    """
    Client Class.

    This class is in charge of sending messages to the unique server.
    All data sent and recieved is packed in the following form

            byte byte byte byte byte

    that means the whole on wire structure is 5 bytes length. Each byte stores
    the desired angle for each finger, following the indexes declared in
    common.py, and each finger values can have values from 0 - 180.
    The first byte have a double pourpose, since we use active discovering from
    client side, if the first byte have a 255 value, that means that the
    client is handshaking the server, so the server replies back to client.
    """

    def __init__(self, 
                 server_ip="", 
                 server_port=SERVER_PORT,
                 wlan=None,
                 hand_obj=None):
        """
        Client constructor
        Here we initialize the client with all the provided data
        
        ARGS:
            port (int): Server port
            hand_obj (obj): Hand obj (flex sensors)
            wlan: wlan obj

        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None
        self.wlan = wlan
        self.hand = hand_obj
        self.client_id = random.randint(1000, 9999)
    
    def discover_servers(self):
        """
        Discover servers
        This method scans all the network and await for a handshake
        
        ARGS:

        RETURNS:
        """
        my_ip = self.wlan.get_local_ip()
        network_base = '.'.join(my_ip.split('.')[:3]) + '.'
        
        # debug
        # print("Looking for servers...")
        
        sock = None # dummy socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.3)
            sock.bind(('0.0.0.0', 0))  # Bind to random port

            for i in range(1, 255):
                test_ip = network_base + str(i)
                # debug
                # print(f" Testing ip: {test_ip}")

                if test_ip != my_ip:
                    try:
                        # Send handshake
                        ack_data = struct.pack('BBBBB', HANDSHAKE,0,0,0,0)
                        sock.sendto(ack_data, (test_ip, SERVER_PORT))
                    
                        # Wait response
                        response, addr = sock.recvfrom(PAYLOAD_LEN)
                        time.sleep(0.5)
                        if struct.unpack('BBBBB', response)[0] == HANDSHAKE:
                            # debug
                            # print(f"Server found: {test_ip}")
                            sock.close()
                            gc.collect()
                            return test_ip
                        
                    except Exception as e:
                        time.sleep(0.5)
                        continue
        
            print("No server found")
            return None
        except Exception as e:
            print(f"Fatal error while scanning the network: {e}")
            return None

    def start(self):
        """
        Start client
        This method initializes the client by looking for an active server and
        stablishing a udp connection with it. After that, the client will 
        read values from the sensor and send all the values to server.
        
        ARGS:

        RETURNS:
        """

        self.server_ip = self.discover_servers()

        if not self.server_ip:
            sys.exit()

        # Create UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.2)
        
        # debug
        #print(f"Client {self.client_id} started. "
        #"Server: {self.server_ip}:{self.server_port}")

        while True:
            try:
                # Read data from fingers, pack it and send it
                msg = struct.pack('BBBBB', 
                                  self.hand.read_finger_data(INDEX_ID), 
                                  self.hand.read_finger_data(MIDDL_ID),
                                  self.hand.read_finger_data(RINGF_ID),
                                  self.hand.read_finger_data(PINKY_ID),
                                  self.hand.read_finger_data(THUMB_ID))
                self.send_message(msg)
                gc.collect()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
    
    def send_message(self, message):
        """
        Send message
        This method send a message to the serverr.
        
        ARGS:
            message: Message to send
        RETURNS:
        """
        try:
            self.sock.sendto(message, (self.server_ip, self.server_port))
        except Exception as e:
            print(f"FATAL ERROR WHILE SENDING MESSAGE: {e}")
