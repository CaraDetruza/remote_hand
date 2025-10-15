from misc import SERVO_FINGER_PINS, SERVO_PIN_IDX
from finger_servo import finger_servo

class hand_servo():
    """
    Hand Servo Class.

    This class provides a way to control all the fingers in a generic way.
    The main pourpose of this class is to gather up all the fingers.
    """
    def __init__(self,
                data=None):
        """
        Hand servo constructor
        Here we build all the fingers with the data of shape

                    [(servo pin ,Finger id, finger name)]

        """
        self.fingers = [finger_servo(servo_data) for servo_data in data]
        self.reset_hand()

    def reset_hand(self):
        """
        Reset hand
        This method move the hand to its initial position.

        ARGS:

        RETURNS:
        """
        for servo_f in self.fingers:
            servo_f.reset()

    def move_hand(self, data):
        """
        Move hand
        This method move the hand to a desired position. The method recieves a
        data arg with shape

            (fngr_angl, fngr_angl, fngr_angl, fngr_angl, fngr_angl)

        each one follow the indexes declared in common.py

        ARGS:
            data (tuple): Tuple with angles of each finger
            
        RETURNS:
        """
        for f_idx, val in enumerate(data):
            self.fingers[f_idx].move_finger(val)
