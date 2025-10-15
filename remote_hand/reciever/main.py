from misc import sleep_ms, WIFI_CREDENTIALS, sys, SERVO_FINGER_PINS
from wifi_driver import wifi_driver as wifi
from server import UDPServer
from hand_servo import hand_servo

if __name__ == "__main__":

    # Build servo hand
    HAND = hand_servo(SERVO_FINGER_PINS)

    # Create and start server
    server = UDPServer(servo_hand=HAND)
    server.start()
    

