from machine import Pin, PWM
from common.misc import SERVO_PWM_FREQ, SERVO_MIN_U16_DUTY, \
    SERVO_MAX_U16_DUTY, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE, \
    SERVO_CURRENT_ANGLE

class servo:
    """
    Servo Class.

    This class is in charge of controling the raw servo.
    """

    def __init__(self, pin):
        """
        Servo constructor
        Here we initialize the servo.

        ARGS:
            pin (int): Servo pin

        """
        self.__servo_pwm_freq = SERVO_PWM_FREQ
        self.__min_u16_duty = SERVO_MIN_U16_DUTY
        self.__max_u16_duty = SERVO_MAX_U16_DUTY
        self.min_angle = SERVO_MIN_ANGLE
        self.max_angle = SERVO_MAX_ANGLE
        self.current_angle = SERVO_CURRENT_ANGLE
        self.__initialise(pin)

    def move(self, angle):
        """
        Move servo
        This method change the servo angle

        ARGS:
            angle (int): Desired angle

        RETURNS:
        """
        angle = round(angle, 2)
        # If same angle or angle dont change too much we dont move
        if angle == self.current_angle or abs(angle - self.current_angle) < 10:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)
    
    def stop(self):
        """
        Stop servo
        This method stop the servo

        ARGS:

        RETURNS:
        """
        self.__motor.deinit()
    
    def get_current_angle(self):
        """
        Current angle getter

        ARGS:

        RETURNS:
            current angle in degrees
        """
        return self.current_angle

    def __angle_to_u16_duty(self, angle):
        """
        Map angle to u16 value
        This method maps the servo angle to the u16 value

        ARGS:
            angle (int): Angle to map

        RETURNS:
            int: mapped value
        """
        return int((angle - self.min_angle) * self.__angle_conversion_factor) \
            + self.__min_u16_duty


    def __initialise(self, pin):
        """
        Initialize
        This method initializes the servo for a desired pin

        ARGS:
            pin (int): Servo pin

        RETURNS:
        """
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - \
                                          self.__min_u16_duty) / \
                                            (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
