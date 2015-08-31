import random
import re

class BasicDiceRoller(object):
    ALIAS = ("normal",)
    DICE_RE = re.compile(r'((?P<number>[0-9]+)|a\s+)?d(?P<sides>[0-9]+|%)?\b')
    MOD_RE = re.compile(r'\s*(?P<modifier>(\+|-)\s*([0-9]+))\b')

    def __init__(self, default=6):
        self.default_sides = 6

    def _roll(self, number=1, sides=None):
        if sides is None:
            sides = self.default_sides
        elif sides == '%':
            sides = 100

        sides = int(sides)

        if number is None:
            number = 1

        number = int(number)

        for i in range(number):
            yield random.randint(1, sides)

    def _total(self, rolls, modifier=None):
        total = sum(rolls)
        if modifier is not None:
            total += int(modifier)

        return total

    def roll(self, number=1, sides=None, modifier=None):
        rolls = list(self._roll(number, sides))
        if modifier is not None:
            return (rolls, self._total(rolls, modifier))
        else:
            return (rolls, None)


class FateDiceRoller(BasicDiceRoller):
    ALIAS = ("fate", "fudge")
    DICE_RE = re.compile(r'((?P<number>[0-9]+)|a\s+)?d(?P<sides>[0-9]+|%|F)?\b')

    def _roll(self, number=1, sides='F'):
        # fudge has 3 types of sides
        if sides not in ('F', None):
            for r in super(FateDiceRoller, self).roll(number, sides):
                yield r

        number = int(number)

        for i in range(number):
            yield random.randint(-1, 1)

    def roll(self, number=1, sides=None, modifier=None):
        rolls = list(self._roll(number, sides))
        if modifier is not None or sides in ('F', None):
            return (rolls, self._total(rolls, modifier))
        else:
            return (rolls, None)
