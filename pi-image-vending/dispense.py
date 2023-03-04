#!/usr/bin/python
import requests
from time import sleep

try: 
    import RPi.GPIO as GPIO
except ImportError: 
    GPIO = None


def get_txns(from_block):
	return requests.get('https://zksync2-testnet-explorer.zksync.dev/transactions', params={'limit': '10', 'fromBlockNumber': str(from_block), 'direction': 'newer', 'accountAddress': '0x8411Ec26D6Eb5013C2080366C88602716eAa41F3'}).json()

last_block = None

try:
	last_block = get_txns('1540').get('list')[-1]['blockNumber'] + 1
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

def get_txn_data_from_last_block():
	global last_block
	new_txns = get_txns(last_block)
	print('new_txns', new_txns)
	if not new_txns.get('list') or not len(new_txns['list']):
		return []
	last_block = new_txns['list'][-1]['blockNumber'] + 1
	print('new last block = ', last_block)
	return [t for t in new_txns['list']]

new_txns = []

def dispense_coin():
	if not GPIO:
		print('dispensing but skipping gpio')
		return
	GPIO.output(channel, GPIO.HIGH)
	sleep(0.1)
	GPIO.output(channel, GPIO.LOW)
	print('dispensed')
	sleep(20)
	print('dispense done')

while True:
	print('at block', last_block)
	new_txns += get_txn_data_from_last_block()
	while len(new_txns):
		print(new_txns)
		print('has txn', new_txns.pop())
		dispense_coin()
	sleep(10)

# Reset all gpio pin
GPIO.cleanup()
