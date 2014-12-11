entropic
========

A simple utility for creating [high entropy](http://www.contravex.com/2014/03/14/on-making-high-entropy-bitcoin-paper-wallets/) bitcoin private keys.

## Usage:

1. Roll 5 six-sided [casino dice](http://www.amazon.com/Trademark-Poker-Grade-Serialized-Casino/dp/B000RQ0GLU/) at least 6 times (each roll adds one word, equal to [12.9 bits of entropy](https://en.wikipedia.org/wiki/Diceware))
2. With each roll append the results in the command line, like so: `python3 main.py 351456135165132154654651324654321324646312654651321654632165`
3. Print or write down the back up phrase contained within the single quotes
4. Import the private key into your favorite wallet software

## Deterministic addresses:

Entropic allows you to create deterministic keys based on your back up phrase. Use the `-n` or `--numaddrs` option to specify how many keys to make. For example:

`python3 main.py 351456135165132154654651324654321324646312654651321654632165 -n 3`

This would produce 3 private keys based on the following phrases:

* 'ka toast yh busy pugh ewe gulf puck avail yh chump guyana'
* 'ka toast yh busy pugh ewe gulf puck avail yh chump guyana1'
* 'ka toast yh busy pugh ewe gulf puck avail yh chump guyana2'

## Why use casino dice?

See [here](http://www.dakkadakka.com/wiki/en/That%27s_How_I_Roll_-_A_Scientific_Analysis_of_Dice). Thanks [ferretinjapan](http://www.reddit.com/user/ferretinjapan)!