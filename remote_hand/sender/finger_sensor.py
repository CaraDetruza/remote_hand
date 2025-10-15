import sys
from machine import Pin, ADC
from common.misc import FINGER_ID_IDX, NAME_IDX, FLEX_SENSOR_PIN_IDX, \
    LED_PIN_IDX, SENSOR_MAX_VAL, SENSOR_MIN_VAL, MAX_CALIBRATION_STEPS, \
    LED_HIGH, LED_LOW, MAX_DEG, MIN_DEG, sleep_ms

class finger_sensor:
    """
    Finger class.

    This class will store all finger data
    and send it to the reciever providing
    a smoth and uniform way of communication.
    """
    def __init__(self, 
                 data=None):
        """
        Constructor.
        This constructor recieves a data tuple for finger creation.
        If data is not correct, the program crashes.

        ARGS:
            data (tuple) -> Tuple with shape (1, 3), this tuple contains
                    finger builder data structured in following
                    way:
                        (FINGER_ID, FINGER_NAME, FLEX_PIN, LED_PIN)

        RETURNS:

        """

        # Not necesary cuz builder data is hardcoded but
        # perform sanity checks is always fine :)
        if data is None:
            sys.exit()

        self.finger_id = data[FINGER_ID_IDX]
        self.name = data[NAME_IDX]
        self.flex_pin = data[FLEX_SENSOR_PIN_IDX]
        self.led_pin = data[LED_PIN_IDX]
        self.led = Pin(self.led_pin, Pin.OUT)
        self.led.value(LED_LOW)

        self.adc = None
        self.read = None

        self.min_val = SENSOR_MAX_VAL
        self.max_val = SENSOR_MIN_VAL

        self.build_finger()
        self.calibrate()

    def build_finger(self):
        """
        Build finger.
        This method initializes the adc attribute which is the way in which
        the data from flex sensor is readen.

        ARGS:

        RETURN:

        """
        self.adc = ADC(Pin(self.flex_pin))
        self.adc.atten(ADC.ATTN_11DB)

    def read_raw_val(self):
        """
        Read raw value.
        This method will return a raw value measured by the adc from the
        flex sensor.

        ARGS:

        RETURN:
            value (Int) -> Raw sensor value
        """
        self.read = self.adc.read()
        return self.read
    
    def angle(self):
        """
        Angle Mapping Function.
        This method maps a value read by the sensor into the angle value to 
        send it to reciever

        ARGS:

        RETURN:
            angle (int) -> angle value
        """
        angle = 0
        try:
            angle = (self.read_raw_val() - self.min_val) * \
            (MAX_DEG - MIN_DEG) / (self.max_val - self.min_val) + MIN_DEG
        except Exception as e:
            print(f"Error: {e}")
        if angle < 0: angle = 0
        if angle > 180: angle = 180
        return round(angle)

    def get_name(self):
        """
        Name getter.
        Returns finger name

        ARGS:

        RETURN:
            name (String) -> Finger's name
        """

        return self.name
    
    def calibrate(self):
        """
        Finger Calibration Method.
        This method calibrates the finger by reading values while bend and
        unbend the finger, giving a range of values corresponding to the
        minimum possible value and max possible value. This info is crucial
        for the correct mapping to the corresponding degree.

        ARGS:

        RETURN:

        """

        self.led.value(LED_HIGH)
        sleep_ms(500)
        self.led.value(LED_LOW)

        step = 0
        while  step < MAX_CALIBRATION_STEPS:
            curr_val = self.read_raw_val()
            if curr_val < self.min_val:
                self.min_val = curr_val
                
            if curr_val > self.max_val:
                self.max_val = curr_val
                
            sleep_ms(125)

            step += 1

    def debug(self):
        """
        Debug Method.
        This method return as string all the useful info of the finger.

        ARGS:

        RETURN:
            dbg_str (str): debug string
        """
        dbg_str = "name: {fname} -> read {fread} ({deg_val}deg) [{minv}, " \
        "{maxv}]".format(
                       fname=self.get_name(),
                       fread=self.read_raw_val(), 
                       deg_val=self.angle(), 
                       minv=self.min_val,
                       maxv=self.max_val
                   )
        
        return dbg_str
