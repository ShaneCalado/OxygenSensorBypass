# This program runs on a Raspberry Pi 3.
# It reads the output signal of a downstream O2 sensor and sends a modified value back to the ECU.
# This can be used to eliminate a check-engine-light on a malfunctioning sensor, or modify the
# sensor's output to influence performance and fuel economy

# Import Raspberry PI GPIO module
import RPi.GPIO as GPIO


global modifiedMode
global voltageMod

# 0 > Copy input voltage to output pin
# 1 > Modify inout voltage by set amount (voltageMod)
# 2 > Modify voltage by (voltageMod) percent
modifiedMode = 0
# Safe range is between 0 and 3.3v
voltageMod = 0

# Initialize GPIO interface
GPIO.setmode(GPIO.BOARD)

# Reset all pins to original state
GPIO.cleanup()

# Define IO pins
# pin 5, is input
GPIO.setup(5, GPIO.IN, pull_up_daown=GPIO.PUD_DOWN)
# pin 6 is output
GPIO.setup(6, GPIO.OUT)

# Function to read the input voltage of pin 5, and output it to pin 6
def copyInputSignal():
    # Read inout from pin 5
    inputPinSignal = GPIO.input(5)
    # Output to pin 6
    GPIO.output(6, inputPinSignal)

# Function to read the input voltage of pin 5, modify it by a fixed amount, and output it to pin 6
def modifyInputSignalFixed(int):
    # Read input from pin 5
    inputPinSignal = GPIO.input(5)
    newInputSignal = inputPinSignal + voltageMod
    # if the new voltage is within a safe range send it to output, otherwise output unmodified voltage
    if newInputPinSignal <= GPIO.HIGH and newInputPinSignal >= GPIO.LOW:
        GPIO.output(6, newInputPinSignal)
    else:
        GPIO.output(6, inputPinSignal)

# Function to read the input voltage of pin 5, modify it by a percent, and output it to pin 6
def modifyInputSignalPercent(int):
    # Read input from pin 5
    inputPinSignal = GPIO.input(5)
    newInputSignal = inputPinSignal * (voltageMod / 100)
    # if the new voltage is within a safe range send it to output, otherwise output unmodified voltage
    if newInputPinSignal <= GPIO.HIGH and newInputPinSignal >= GPIO.LOW:
        GPIO.output(6, newInputPinSignal)
    else:
        GPIO.output(6, inputPinSignal)

# While receiving input from pin 5 (engine is running, O2 sensor sending signal)
while GPIO.input(5) >= GPIO.HIGH:
    if modifiedMode == 0:
        # Copy input to output
        copyInputSignal()
    elif modifiedMode == 1:
        # modified signal
        modifyInputSignalFixed(voltageMod)
    elif modifiedMode == 2:
        # modified signal 
        modifyInputSignalPercent(voltageMod)
    else:
        # invalid mode