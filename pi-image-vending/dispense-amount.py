#!/usr/bin/python
import requests
from time import sleep
import os

try: 
    import RPi.GPIO as GPIO
except ImportError: 
    GPIO = None


base = os.environ['base']
token = os.environ['token']
account = os.environ['account']
per_token = int(os.environ['per_token'])


def get_balance():
	url = f'https://{base}/api?module=account&action=tokenlist&address={account}'
	for element in requests.get(url).json()['result']:
		if element['contractAddress'].lower() == token.lower():
			return int(element['balance'])
	return 0

balance = 0

try:
	balance = get_balance() - per_token
	if balance < 0:
		balance = 0
except:
	print('no block')

if GPIO:
	print('gpio setup')
	# Set GPIO mode: GPIO.BCM or GPIO.BOARD
	GPIO.setmode(GPIO.BCM)

	channel = 6

	# Set mode for each gpio pin
	GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)

print('setup')

new_txns = []

def dispense_coin():
	if not GPIO:
		print('dispensing but skipping gpio')
		return
	GPIO.output(channel, GPIO.HIGH)
	sleep(0.1)
	GPIO.output(channel, GPIO.LOW)
	print('dispensed')
	sleep(3)
	print('dispense done')

print(f'has balance {balance}')
while True:
	try:
		new_balance = get_balance()
		if new_balance != balance:
			print(f'new_balance {new_balance}, balance {balance}')
		while new_balance - balance > 0:
			print(f'has {new_balance} from {balance}')
			dispense_coin()
			balance += per_token
		sleep(10)
	except KeyboardInterrupt:
		break


if GPIO:
	# Reset all gpio pin
	GPIO.cleanup()

print('shutting down')
