from .misc import sleep_ms, WIFI_TIME_SLEEP_MS
import network

class wifi_driver():
    """
    Wifi Driver Class.

    This class helps the ESP32/micropython device to connect
    to the wifi network.
    """
    def __init__(self, 
                 ssid="",
                 password=""):
        """
        Wifi driver constructor
        Here we set the SSID, PASS and the network obj and initiale objs
        """

        self.SSID = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
    def is_connected(self):
        """
        Is connected?
        This method tells if device is already connected to a wifi network.

        ARGS:

        RETURNS:
            boolean - True if connected, FAlse if not connected
        """
        return self.wlan.isconnected()
    
    def get_local_ip(self):
        """
        Is connected?
        This method tells if device is already connected to a wifi network.

        ARGS:

        RETURNS:
            boolean - True if connected, FAlse if not connected
        """
        return self.wlan.ifconfig()[0]
        
    def connect(self):
        """
        Connect device
        Connect device to wifi

        ARGS:

        RETURNS:
            str: Local ip
        """

        # Counter to register number of attemps
        try_no = 0
        found = False

        # Try to connect until its connected
        while not self.is_connected():
            try_no += 1
            if not found:
                wifiList = self.wlan.scan()
                for item in wifiList:
                    if str(item[0].decode('utf-8')) == self.SSID:
                        found = True
            try:
                self.wlan.connect(self.SSID, self.password)
            except OSError as e:
                print(e)
            sleep_ms(WIFI_TIME_SLEEP_MS)
        return self.get_local_ip()
