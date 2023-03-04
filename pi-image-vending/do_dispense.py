#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import os


time_ms = int(os.environ['TIME_MS'] or '100')

print('gpio setup')
# Set GPIO mode: GPIO.BCM or GPIO.BOARD
GPIO.setmode(GPIO.BCM)

channel = 6

# Set mode for each gpio pin
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)


def dispense_coin():
	if not GPIO:
		print('dispensing but skipping gpio')
		return
	GPIO.output(channel, GPIO.HIGH)
	sleep(time_ms / 1000)
	GPIO.output(channel, GPIO.LOW)
	print('dispensed')
	sleep(5)
	print('dispense done')

dispense_coin()
GPIO.cleanup()
