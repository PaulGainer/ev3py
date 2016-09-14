#!/usr/bin/env python
#===============================================================================
# Template file for EV3 Python Loader
#   - Paul Gainer
#   - Last modified: 15/08/2016
#===============================================================================
from ev3dev.ev3 import Screen, ColorSensor, Leds, Button, Sound, \
    InfraredSensor, TouchSensor, LargeMotor, MediumMotor, \
    OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, \
    INPUT_1, INPUT_2, INPUT_3, INPUT_4
import time, os, sys
from threading import Thread
from Queue import Queue
from multiprocessing import Process

#===============================================================================
# Constants
#===============================================================================
#-------------------------------------------------------------------------------
# Motors
#-------------------------------------------------------------------------------
LEFT = 0
RIGHT = 1
HEAD = 2
#-------------------------------------------------------------------------------
# Sensors
#-------------------------------------------------------------------------------
T_LEFT = 0
T_RIGHT = 1
COLOUR = 2
INFRARED = 3
SENSOR_INFRARED_MAX_RANGE_IN_CM = 50.0
#-------------------------------------------------------------------------------
# Colours
#-------------------------------------------------------------------------------
AMBER = 0
GREEN = 1
ORANGE = 2
RED = 3
YELLOW = 4
#-------------------------------------------------------------------------------
# Musical notes
#-------------------------------------------------------------------------------
C_4 = 0
D_4 = 1
E_4 = 2
F_4 = 3
G_4 = 4
A_4 = 5
B_4 = 6
C_5 = 7
FREQ_C_4 = 261.63
FREQ_D_4 = 293.66
FREQ_E_4 = 329.63
FREQ_F_4 = 349.23
FREQ_G_4 = 392.00
FREQ_A_4 = 440.00
FREQ_B_4 = 493.88
FREQ_C_5 = 523.25
#-------------------------------------------------------------------------------
# Robot verbosity
#-------------------------------------------------------------------------------
ENABLE_SPEECH = True
VERBOSE = False


#===============================================================================
# Classes
#===============================================================================
#-------------------------------------------------------------------------------
# Enum - A class for enumerations
#-------------------------------------------------------------------------------
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

#-------------------------------------------------------------------------------
# CodeProcess - Runs the user's code, and adds a message to the queue upon
#               termination
#-------------------------------------------------------------------------------
class CodeProcess(Process):
    def __init__(self, queue):
        self.queue = queue
        Process.__init__(self)

    def run(self):
        main()
        self.queue.put(0)


#===============================================================================
# Global Variables
#===============================================================================
colour = Enum(["NONE", "BLACK", "BLUE", "GREEN", "YELLOW", "RED", "WHITE",
               "BROWN"])
colours_indexed = [colour.NONE, colour.BLACK, colour.BLUE, colour.GREEN,
                   colour.YELLOW, colour.RED, colour.WHITE, colour.BROWN]
leds_indexed = [Leds.LEFT, Leds.RIGHT]
led_colours_indexed = [Leds.AMBER, Leds.GREEN, Leds.ORANGE, Leds.RED,
                       Leds.YELLOW]
frequencies_indexed = [FREQ_C_4, FREQ_D_4, FREQ_E_4, FREQ_F_4, FREQ_G_4,
                       FREQ_A_4, FREQ_B_4, FREQ_C_5]
function_list = REPLACE_ME_LIST_OF_FUNCTIONS
button = Button()
screen = Screen()
sound = Sound()
message_queue = Queue(maxsize = 1)

#===============================================================================
# Functions
#===============================================================================
#-------------------------------------------------------------------------------
# motor_and_sensor_check - checks that all motors and sensors are present and
#                          have been correctly configured
#-------------------------------------------------------------------------------
def motor_and_sensor_check():
    global motors, sensors
    motors = [None] * 3
    sensors = [None] * 4
    error = ""
    try:
        motors[LEFT] = LargeMotor(REPLACE_ME_LEFT)
        if not motors[LEFT].connected:
            raise Exception()
    except Exception as e:
        error += "There was a problem initialising the left motor.\n"
    try:
        motors[RIGHT] = LargeMotor(REPLACE_ME_RIGHT)
        if not motors[RIGHT].connected:
            raise Exception()
    except Exception as e:
        error += "There was a problem initialising the left motor.\n"
    try:
        motors[HEAD] = MediumMotor(REPLACE_ME_HEAD)
        if not motors[HEAD].connected:
            raise Exception()
    except Exception as e:
        error += "There was a problem initialising the head motor.\n"
    try:
        sensors[COLOUR] = ColorSensor()
        if not sensors[COLOUR].connected:
            raise Exception()
    except Exception as e:
        error += "No colour sensor connected.\n"
    try:
        sensors[INFRARED] = InfraredSensor()
        if not sensors[INFRARED].connected:
            raise Exception()
    except Exception as e:
        error += "No infrared sensor connected.\n"
    try:
        sensors[T_LEFT] = TouchSensor(REPLACE_ME_T_LEFT)
        if not sensors[T_LEFT].connected:
            raise Exception()
    except Exception as e:
        error += "No left touch sensor connected to sensor port " + \
                 "REPLACE_ME_T_LEFT" + "."
    try:
        sensors[T_RIGHT] = TouchSensor(REPLACE_ME_T_RIGHT)
        if not sensors[T_RIGHT].connected:
            raise Exception()
    except Exception as e:
        error += "No right touch sensor connected to sensor port " + \
                 "REPLACE_ME_T_RIGHT" + "."
    if error:
        raise Exception(error)

#-------------------------------------------------------------------------------
# validate_parameters - validates the number of function arguments, and the type
#                       of the arguments
#-------------------------------------------------------------------------------
def validate_parameters(name, *args):
    flist = [n for n, tuple in enumerate(function_list) if
             tuple[0] == name]
    if flist:
        findex = flist[0]
        fname, fdescription, param_list, fcode = \
            function_list[findex]
        args_list = list(args)
        if len(args_list) != len(param_list):
            raise Exception("Expected " + \
                            (str(len(param_list)), "no")[
                                len(param_list) ==
                                0] + \
                            " argumment" + ("s", "")[
                                len(param_list) == 1] + \
                            " for function \'" + fname + "\'")
        aindex = 0
        for param in param_list:
            arg = args_list[aindex]
            pname, type, min, max, pdescription = param
            type = eval(type)
            min = eval(min)
            max = eval(max)
            error = "Invalid value for parameter \'" + pname + \
                    "\' passed to function \'" + fname + "\':\n"
            if not isinstance(arg, type):
                raise Exception(
                    error + "    received instance of type " + \
                    args_list[aindex].__class__.__name__ + \
                    "\n    expected instance of type " + \
                    type.__name__ + "\n" + fdescription)
            if type == int:
                if (min != None) & (max != None) & (
                    (arg < min) | (arg > max)):
                    raise Exception(
                        error + "    expected an int in the range " + \
                        str(min) + "-" + str(max))
                elif (min != None) & (arg < min):
                    raise Exception(
                        error + "    expected an int greater than " + \
                        "equal to " + str(min))
                elif (max != None) & (arg > max):
                    raise Exception(
                        error + "    expected an int less than or " + \
                        " equal to " + str(max))
            aindex = aindex + 1

#-------------------------------------------------------------------------------
# Inserted functions from the XML file
#-------------------------------------------------------------------------------
REPLACE_ME_FUNCTIONS

#-------------------------------------------------------------------------------
# Inserted main() function
#-------------------------------------------------------------------------------
REPLACE_ME_MAIN

#-------------------------------------------------------------------------------
# init - Initialises the motors and sensors
#-------------------------------------------------------------------------------
def init():
    motor_and_sensor_check()
    sensors[COLOUR].mode = 'COL-COLOR'
    sensors[INFRARED].mode = 'IR-PROX'

#-------------------------------------------------------------------------------
# Entry point
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    is_initialisation = (len(sys.argv) == 2) and (
    sys.argv[1] == '-init')
    code_proc = CodeProcess(message_queue)
    try:
        init()
        if is_initialisation and VERBOSE:
            sound.beep()
        if not is_initialisation:
            #code_proc.daemon = True
            code_proc.start()
            message_queue.join()
            while (not button.backspace) and message_queue.empty():
                pass
            if not message_queue.empty():
                message_queue.get()
    except Exception as error:
        if is_initialisation:
            print str(error)
            os.remove(sys.argv[0])
        else:
            os.system('clear')
            if VERBOSE and ENABLE_SPEECH:
                sound.speak("There was an error")
            print str(error)
            while not button.any():
                pass
    finally:
        if code_proc.is_alive():
            code_proc.terminate()
