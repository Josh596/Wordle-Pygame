import json
from enum import Enum

LENGTH_WORD = 5
MAX_GUESSES = 6

alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

with open('words.json') as f:
    WORD_LIST = json.load(f)


class State(Enum):
    FAIL = 0
    SUCCESS = 1
    NEUTRAL = 2