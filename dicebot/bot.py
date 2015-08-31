import inspect
import re

from dicebot import roller


class TextHandler(object):
    MATCHERS = {
        'emote': {
            re.compile(r'^rolls\s+(.+)$'): '_process_dice',
        },
        'text': {
            re.compile(r'use ((d(?P<num1>[0-9]+)s?)|((?P<num2>[0-9]+)-sided dice)) by default'): '_set_default_sides',
            re.compile(r'use (.+) dice(?! by default)'): '_set_roller',
        }
    }

    AVAILABLE_ROLLERS = {}

    def __init__(self):
        self.roller = self.AVAILABLE_ROLLERS['normal']()

    def process_text(self, fmt, text):
        message_type = None
        message_match = None
        for matcher, target in self.MATCHERS[fmt].items():
            m = matcher.match(text)
            if m is not None:
                message_type = target
                message_match = m
                break

        if message_type is None:
            return None

        f = getattr(self, message_type)
        res = f(message_match.group(1), match=message_match)

        # TODO: format this
        return res

    def _set_roller(self, roller_type, match):
        self.roller = self.AVAILABLE_ROLLERS[roller_type]()
        return EmoteResponse('uses {0} dice'.format(roller_type))

    def _set_default_sides(self, raw_sides_str, match):
        self.roller.default_sides = match.group('num1') or match.group('num2')
        return EmoteResponse('gets some {0}'.format(raw_sides_str))

    def _process_dice(self, dice_str, match):
        dice_match = self.roller.DICE_RE.match(dice_str)
        if dice_match is None:
            return None

        rest = dice_str[dice_match.end():]
        mod_match = self.roller.MOD_RE.match(rest)

        if mod_match is None:
            return DiceResponse(self.roller.roll(dice_match.group('number'), dice_match.group('sides'), None), None)
        else:
            return DiceResponse(self.roller.roll(dice_match.group('number'), dice_match.group('sides'), mod_match.group('modifier')), mod_match.group('modifier'))


for name, cl in inspect.getmembers(roller):
    if inspect.isclass(cl):
        for alias in cl.ALIAS:
            TextHandler.AVAILABLE_ROLLERS[alias] = cl


class DiceResponse(object):
    TYPE = 'text'

    def __init__(self, raw_resp, modifier=None):
        self.raw_resp = raw_resp
        self.modifier = modifier

    def __str__(self):
        str_rolls = (str(r) for r in self.raw_resp[0])
        modifier_str = ''
        if self.modifier is not None:
            modifier_str = ' [{0}]'.format(self.modifier)

        if self.raw_resp[1] is not None:
            return 'You rolled {rolls}{mod} to get {total}'.format(rolls=' + '.join(str_rolls), mod=modifier_str, total=self.raw_resp[1])
        else:
            return 'You rolled {rolls}'.format(rolls=', '.join(str_rolls))


class EmoteResponse(object):
    TYPE = 'emote'

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content
