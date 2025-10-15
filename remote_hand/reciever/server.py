import socket
import network
import time
from machine import Pin
from common.misc import SERVER_PORT, PAYLOAD_LEN, HANDSHAKE
import struct
from hand_servo import hand_servo

class UDPServer:
    """
    Server Class.

    This class is in charge of recieving all the messages sent by the client/
    sender. UDP is used since is a good option for rapid data tranmision and
    ib better than using BT.
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
                 port=SERVER_PORT,
                 servo_hand=None):
        """
        Server constructor
        Here we initialize the server with the required data.

        ARGS:
            port (int): Server port
            servo_hand (obj): Hand obj

        """
        self.port = port
        self.sock = None
        self.servo_hand = servo_hand
    
    def start(self):
        """
        Start server
        This method initializes the socket and start listening to active conns
        and proccess the recieved messages.

        ARGS:

        RETURNS:
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.setblocking(False)
        
        while True:
            try:
                self.check_messages()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")
    
    def check_messages(self):
        """
        Start server
        This method initializes the socket and start listening to active conns
        and proccess the recieved messages.

        ARGS:

        RETURNS:
        """
        try:
            # Recieve 5 bytes
            data, addr = self.sock.recvfrom(PAYLOAD_LEN)

            if data:
                # debug
                #print(f"[{addr[0]}] -> {data}")
                
                # Proccess cmd
                response = self.process_command(data)

                # If handshake we reply back to client
                if response:
                    self.sock.sendto(response, addr)
                
                time.sleep(0.1)
                
        except OSError as e:
            if e.args[0] != 11: 
                print(f"Socket error: {e}")
    
    def process_command(self, data):
        """
        Process command
        This method unpack the recieved data and decide if we are dealing with a
        handshake or regular command, and decide how to do in each case.

        ARGS:
            data: recieved raw data

        RETURNS:
        """
        cmd = struct.unpack('BBBBB', data)
        # debug
        #print(cmd)
        if cmd[0] == 255:
            response = struct.pack('BBBBB', 255,0,0,0,0)
            return response
        else:
            self.servo_hand.move_hand(cmd)
