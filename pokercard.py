POKERCARDS_VALUE_DICT = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

POKERCARDS_SUIT_DICT = {
    "Spades": {"suit": 1, "displayed_suit": "♤"}, 
    "Hearts": {"suit": 2, "displayed_suit": "♡"}, 
    "Diamonds": {"suit": 3, "displayed_suit": "♢"}, 
    "Clubs": {"suit": 4, "displayed_suit": "♧"}
}

class PokerCard:
    def __init__(self, value: str, suit: str):        
        self.displayed_value = value
        self.displayed_suit = POKERCARDS_SUIT_DICT[suit]["displayed_suit"]
        self.value = POKERCARDS_VALUE_DICT[value]
        self.suit = POKERCARDS_SUIT_DICT[suit]["suit"]

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __repr__(self):
        return self.displayed_value + self.displayed_suit

def index_all(source, value_to_find):
    return [i for i, x in enumerate(source) if x == value_to_find]