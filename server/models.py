from enum import Enum
import random 



class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class CardValue(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class CardSuit(Enum):
    CLUB = 0
    HEART = 1
    DIAMOND = 2
    SPADE = 3


class Card:

    def __init__(self, suit, value):
        self._value = value
        self._suit = suit

    def __repr__(self):
    	return (self.__str__())

    def __str__(self):
    	return (str(self._value) + " " + str(self._suit))

    @property
    def value(self):
        return self._value

    @property
    def suit(self):
        return self._suit


    def __lt__(self, other):
        return self._value < other._value

    def __gt__(self, other):
        return self._value > other._value
        


class Deck:
    def __init__(self):
        suits, numbers = range(0,4), range(1,14)
        self.deck = random.sample([Card(CardSuit(a),CardValue(b)) for a in suits for b in numbers], k=len(suits) * len(numbers))
        self.deck_index = 0

    def next(self):
        ret = self.deck[self.deck_index]
        self.deck_index += 1
        return ret

class PlayerStatus(Enum):
    PLAYING = 0
    FOLDED = 1
    SITTINGOUT = 2


class Action(Enum):
    FOLD = 0
    CHECK = 1
    CALL = 2
    BET = 3
    RAISE = 4


class Street(Enum):
    DEALING = 0
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

class HandType(OrderedEnum):
    HIGHCARD = 0
    PAIR = 1
    TRIPS = 2
    STRAIGHT = 3
    FLUSH = 4
    FULLHOUSE = 5
    QUADS = 6
    STRAIGHTFLUSH = 7

class Move(Enum):
	FOLD = 0
	CHECK = 1
	CALL = 2
	BET = 3
	RAISE = 4

class Hand(object):
    def __init__(self, hand_type, value):
        self.hand_type = hand_type
        self.value = value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.hand_type == other.hand_type and self.value == self.value
    
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            if (self.hand_type > other.hand_type):
                return True
            elif (self.hand_type == other.hand_type):
                return self.value > other.value
        return False
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if (self.hand_type < other.hand_type):
                return True
            elif (self.hand_type == other.hand_type):
                return self.value < other.value
        return False

