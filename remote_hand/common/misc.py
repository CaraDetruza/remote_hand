from time import sleep_ms
import sys

"""
File with common constants
"""

# these defaults work for the standard TowerPro SG90
SERVO_PWM_FREQ = 50
# SG90 works from 2% to 12%
SERVO_MIN_U16_DUTY = 1311 # 2% of 2^16
SERVO_MAX_U16_DUTY = 7864 # 12% of 2^16
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
SERVO_CURRENT_ANGLE = 0.001

# WiFi driver time sleep
WIFI_TIME_SLEEP_MS = 2000

# Max and min values that the sensor could have
SENSOR_MAX_VAL = 4096
SENSOR_MIN_VAL = 0
MAX_CALIBRATION_STEPS = 25
MIN_DEG = 0
MAX_DEG = 180

# Harcoded indexes for tuple elems
FINGER_ID_IDX = 0
NAME_IDX = 1
FLEX_SENSOR_PIN_IDX = 2
LED_PIN_IDX = 3

# FINGER IDS. This ids will support a correct comms among the sender
# and reciever.
THUMB_ID = 0
INDEX_ID = 1
MIDDL_ID = 2
RINGF_ID = 3
PINKY_ID = 4

# Hardcoded data for buildin finger objects. Each finger object will contain the
# finger sensed data to send this data to reciever. Each tuple elem have the 
# following shape:
#
# (FINGER_ID, NAME, FLEX_SENSOR_PIN, LED_PIN)
FINGERS_BUILD_DATA = [(THUMB_ID, "THUMB", 34, 13), 
                      (INDEX_ID, "INDEX", 35, 12),  
                      (MIDDL_ID, "MIDDLE", 32, 14), 
                      (RINGF_ID, "RING", 33, 22),
                      (PINKY_ID, "PINKY", 36, 23)]

SERVO_PIN_IDX = 1
FINGER_ID_IDX = 0
FINGER_NAME_IDX = 2

INDEX_SERVO = 0
MIDDL_SERVO = 1
RINGF_SERVO = 2
PINKY_SERVO = 3
THUMB_SERVO = 4
ANGLT_SERVO = 5
SERVO_FINGER_PINS = [(INDEX_SERVO, 0, "INDEX"), 
                      (MIDDL_SERVO, 1, "MIDDLE"),  
                      (RINGF_SERVO, 2, "RING"), 
                      (PINKY_SERVO, 3, "PINKY"),
                      (THUMB_SERVO, 4, "THUMB"),
                      (ANGLT_SERVO, 5, "THUMB_ANGLE")]

# Led values
LED_HIGH = 1 
LED_LOW = 0

# Wifi credentials
WIFI_CREDENTIALS = {
    "SSID": "Totalplay-92B0",
    "PASS": "92B07046hTFe8mnj"
}

SERVER_PORT = 5000

# Message length in bytes
PAYLOAD_LEN = 5

# Handshake value
HANDSHAKE = 255
