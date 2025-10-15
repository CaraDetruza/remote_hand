from servo import servo
from misc import SERVO_PIN_IDX, FINGER_ID_IDX, FINGER_NAME_IDX, \
SERVO_FINGER_PINS, ANGLT_SERVO, INDEX_SERVO

class finger_servo():
    """
    Finger Servo Class.

    This class provides a way to control a single finger in a generic way.
    The fingers are servos, this class provides methods to reset, map
    map angles and move a finger.
    """
    def __init__(self,
                 data=None):
        """
        Finger servo constructor
        Here we set the finger servo with the provided data, which have the
        shape
                    (servo pin ,Finger id, finger name)

        thumb have 2 servos, one for flex angle and other for rotation angle,
        this two angles are mapped when thumb is being evaluated
        """
        self.motor = servo(data[SERVO_PIN_IDX])
        self.motor_angle = None
        self.finger_id = data[FINGER_ID_IDX]
        self.finger_name = data[FINGER_NAME_IDX]

        if self.finger_name == "THUMB":
            self.motor_angle = servo(
                SERVO_FINGER_PINS[ANGLT_SERVO][INDEX_SERVO]
            )
            

    def reset(self):
        """
        Reset finger
        This method move the finger to its initial position.

        ARGS:

        RETURNS:
        """
        self.motor.move(0)
        if self.motor_angle: self.motor_angle.move(45)

    def move_finger(self, angle):
        """
        Move finger
        This method move the finger to a determined angle.

        ARGS:
            angle (int): Desired angle

        RETURNS:
        """
        self.motor.move(angle)
        if self.motor_angle: self.motor_angle.move(self.map_thumb_angle(angle))

    def map_thumb_angle(self, angle):
        """
        Map thumb finger angle
        This method maps the rotation angle for the thumb given a thumb flex
        angle

        ARGS:
            angle (int): Desired angle to map

        RETURNS:
            ret (int): Obtained angle
        """
        ret = 45 + (angle - 0) * (90 - 45) / (180 - 0)
        if ret < 45: ret = 45
        if ret > 90: ret = 90
        return round(ret)
