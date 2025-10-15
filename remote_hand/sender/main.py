from common.misc import sleep_ms, FINGERS_BUILD_DATA, WIFI_CREDENTIALS
from common.wifi_driver import wifi_driver as wifi
from sender.hand_sensor import hand_sensor as hand
from sender.client import UDPClient
import sys

if __name__ == "__main__":
    # Build hand
    HAND = hand(data=FINGERS_BUILD_DATA)
    # Connect to wifi
    WLAN = wifi(ssid=WIFI_CREDENTIALS["SSID"], 
                password=WIFI_CREDENTIALS["PASS"])
    # Check if connected successfully
    ip = WLAN.connect()
    
    if not ip:
        sys.exit()
    
    # Create client and start
    client = UDPClient(wlan=WLAN)
    client.start()
