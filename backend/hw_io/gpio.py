try:
    import RPi.GPIO as GPIO
    test = False                 
except ImportError:
    test = True



class PiGpio:
    pins_to_use = None
    _instance = None

    def OpenPin(self, pin_id):
        if (not test):
            GPIO.output(pin_id, GPIO.LOW)

    def ClosePin(self, pin_id):
        if (not test):
            GPIO.output(pin_id, GPIO.HIGH)
        
    def SetUp(self, pins_to_use: list()):
        print ("Setup")
        if (not test):
            self.pins_to_use = pins_to_use
            GPIO.setup(pins_to_use, GPIO.OUT, initial=GPIO.HIGH)

    def __del__(self):
        if (not test):
            GPIO.cleanup(self.pins_to_use)

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(self):
        if self._instance is None:
            print('Creating new instance')
            self._instance = self.__new__(self)
            if (not test):
                GPIO.setmode(GPIO.BOARD)
        return self._instance