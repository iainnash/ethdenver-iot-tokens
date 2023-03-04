# ETHDenver ERC20 Dispenser Code

This listens to addresses on ZKSync ERA and when ERC20s are deposited at a given address a coin is dispensed.

The coin machines take a 50-100ms pulled low pulse @ 5v using a GPIO on a raspberry pi (pin 6) and a transistor to ensure the 5v won't fry the pi.

This project uses https://balena.io/ to run and monitor the images.
