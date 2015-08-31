A Dicebot for Matrix
====================

An extensible Matrix (https://matrix.org) dicebot.

Running
-------

Requirements:

- Python 2.7 (the Matrix Python SDK supports Python 2 only)
- `matrix-python-sdk` (https://github.com/matrix-org/matrix-python-sdk)

Run dicebot as such:

```
$ ./matrix-dicebot.py --user dicebot --password dicebotpw --server https://your.matrix.server
```

Usage
-----

dicebot detects rolls based on emotes (`/me` actions).
For example, try `/me rolls a d20`.  You can add modifiers
(`/me rolls 2d20 + 10`), as well as percentile dice (`/me rolls a d%`).
You can also change the default dice type by sending a normal message
like so: `@dicebot use d20s by default`.  Then, `/me rolls 2d` is the
same as `/me rolls 2d20`.  Finally, dicebot supports different dice
systems.  At the moment, there is the 'normal' system and the 'fate'/'fudge'
system, which can be switch by messaging as such `@dicebot use fate dice`.
You can then use `/me rolls 6dF`.

dicebot will automatically join rooms that it's invited to, although currently
this only works while dicebot is running, due to the way the Matrix python SDK
works.

Extending dicebot
-----------------

Dicebot is designed to be extensible.  You can add additional backends (for
example to hook up to IRC) or different dice systems (for example, the one
used in WoD).  Take a look at `dicebot.backends` and `dicebot.rollers`
for more information.
