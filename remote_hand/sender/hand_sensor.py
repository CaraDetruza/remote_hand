from sender.finger_sensor import finger_sensor as finger

class hand_sensor:
    """
    Hand class.

    This class will build the hand obj with 5 finger sensors.
    """
    def __init__(self, 
                 data=None):
        """
        Constructor.
        This constructor recieves a data tuple array for finger creation.
        If data is not correct, the program crashes.

        ARGS:
            data ([tuple]) -> Tuple with shape (5, 1, 3), this tuple contains
                    finger builder data structured in following
                    way:
                        (FINGER_ID, FINGER_NAME, FLEX_PIN, LED_PIN)

        RETURNS:

        """

        self.fingers = [finger(f_data) for f_data in data]

    def debug(self):
        """
        Debug Method.
        This method print as string all the useful info for all finger sensors
        in hand obj.

        ARGS:

        RETURN:

        """
        for finger in self.fingers: 
            print(finger.debug())

    def read_finger_data(self, finger_idx):
        
        return self.fingers[finger_idx].angle()

