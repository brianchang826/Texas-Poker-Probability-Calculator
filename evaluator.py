from collections import Counter
from pokercard import PokerCard, index_all

class HandValueEvaluator:
    def __init__(self, hand: list[PokerCard], public_cards: list[PokerCard]):
        self.seven_cards = hand + public_cards
        self.seven_cards_values = [c.value for c in self.seven_cards]
        self.sorted_seven_cards_values = sorted(self.seven_cards_values)
        self.values_counts_counter = Counter(self.seven_cards_values)
        self.values_counts = self.values_counts_counter.most_common()
        self.seven_cards_values_set = list(set(self.seven_cards_values))
        self.sorted_seven_cards_values_set = sorted(self.seven_cards_values_set)
        self.seven_cards_suits = [c.suit for c in self.seven_cards]
        self.seven_cards_suits_set = list(set(self.seven_cards_suits))
        self.straight_value = None

    def determine_handvalue(self) -> list[int]:
        for check in [self._check_straight_flush, self._check_four_of_a_kind, self._check_full_house, self._check_flush, self._check_straight, self._check_three_of_a_kind, self._check_two_pairs, self._check_one_pair, self._check_high_card]:
            result = check()
            if result:
                return result
        return []

    def _check_straight_flush(self):

        # early exits
        if len(self.seven_cards_values_set) < 5:
            return None
        
        
        highest_values = []
        highest_values_alt = []
    
        idx = 0
        while len(self.sorted_seven_cards_values_set) >= (idx + 5):
            five_cards_values = self.sorted_seven_cards_values_set[idx:(idx+5)]
            five_cards_suits = self.seven_cards_suits[idx:(idx+5)]
                
            is_continuous = True
            
            for i in range(0, 4):
                if five_cards_values[i+1] - five_cards_values[i] != 1:
                    is_continuous = False
                    break

            if is_continuous:
                highest_values_alt.append(five_cards_values[4])
            
            if is_continuous and len(set(five_cards_suits)) == 1:
                highest_values.append(five_cards_values[4])
    
            idx += 1

        is_ace_low = all(v in self.seven_cards_values_set for v in [2, 3, 4, 5, 14])
                
        if highest_values_alt:
            self.straight_value = [5, max(highest_values_alt)]
        elif is_ace_low:
            self.straight_value = [5, 5]

        if len(self.seven_cards_suits_set) > 3:
            return None

        is_ace_low_and_is_same_suit = False
        
        if is_ace_low:
            
            is_ace_low_and_is_same_suit = True
    
            suit_counts = Counter(self.seven_cards_suits)
            if suit_counts.most_common(1)[0][1] < 5:
                return None
            
            for v in [2, 3, 4, 5, 14]:
                if is_ace_low_and_is_same_suit:
                    idx = index_all(self.seven_cards_values, v)
                    same_suit = False
                    for i in idx:
                        if self.seven_cards_suits[i] == suit_counts.most_common(1)[0][0]:
                            same_suit = True
                            break
                    if not same_suit:
                        is_ace_low_and_is_same_suit = False
        
        if highest_values: 
            return [9, max(highest_values)]
        elif is_ace_low_and_is_same_suit:
            return [9, 5]
        return None

    def _check_four_of_a_kind(self):
        
        # early exits
        if len(self.seven_cards_values_set) > 4:
            return None
        
        if self.values_counts[0][1] == 4:
            remaining_cards = [c for c in self.seven_cards_values if c != self.values_counts[0][0]]
            return [8, self.values_counts[0][0], max(remaining_cards)]
        return None

    def _check_full_house(self):

        # early exits
        if len(self.seven_cards_values_set) > 4:
            return None

        # check if there are three (or above) cards that has the same value and find the one with the largest value
        three_cards = [count[0] for count in self.values_counts if count[1] == 3]
        if not three_cards:
            return None
            
        highest_three_cards_value = max(three_cards)
    
        # check if there are two (or above) cards that has the same value and find the one with the largest value
        two_cards = [count[0] for count in self.values_counts if count[1] >= 2 and count[0] != highest_three_cards_value]
    
        if not two_cards:
            return None
        
        highest_two_cards_value = max(two_cards)
    
        return [7, highest_three_cards_value, highest_two_cards_value]

    def _check_flush(self):
        if len(self.seven_cards_suits_set) > 3:
            return None
        
        suits_counts = Counter([c.suit for c in self.seven_cards])
        flush = [c.value for c in self.seven_cards if c.suit == suits_counts.most_common()[0][0]]
        if len(flush) >= 5:
            flush.sort()
            idx = len(flush) - 1
            result = [6]
            while idx > -1:
                result.append(flush[idx])
                idx -= 1
            return result
        return None

    def _check_straight(self):
    
        # early exits
        if len(self.seven_cards_values_set) < 5:
            return None
        
        if self.straight_value:
            return self.straight_value
        return None


    def _check_three_of_a_kind(self):
        
        # early exits
        if len(self.seven_cards_values_set) > 5:
            return None
        
        three_cards = [count[0] for count in self.values_counts if count[1] == 3]
        
        if not three_cards:
            return None
            
        highest_three_cards_value = max(three_cards)
    
        remaining_cards = [count[0] for count in self.values_counts if count[0] != highest_three_cards_value]

        return [4, highest_three_cards_value, remaining_cards[0], remaining_cards[1]]

    def _check_two_pairs(self):
        
        # early exits
        if len(self.seven_cards_values_set) > 5:
            return None
        
        two_cards = [count[0] for count in self.values_counts if count[1] == 2]
        
        if len(two_cards) < 2:
            return None
    
        two_cards.sort(reverse=True)
        remaining_cards = [c for c in self.seven_cards_values if c not in two_cards[0:2]]
        return [3, two_cards[0], two_cards[1], max(remaining_cards)]

    def _check_one_pair(self):
        
        # early exits
        if len(self.seven_cards_values_set) > 6:
            return None
        
        pairs = [count[0] for count in self.values_counts if count[1] == 2]
        
        if not pairs:
            return None
        
        highest_pair_value = max(pairs)
    
        remaining_cards = [c for c in self.seven_cards_values if c != highest_pair_value]
    
        remaining_cards.sort()
    
        return [2, highest_pair_value, remaining_cards[4], remaining_cards[3], remaining_cards[2]]

    def _check_high_card(self):
        result = [1]
        idx = 6
        for _ in range(5):
            result.append(self.sorted_seven_cards_values[idx])
            idx -= 1
    
        return result