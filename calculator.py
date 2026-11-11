from itertools import combinations
from collections import Counter
import multiprocessing
import time
from evaluator import HandValueEvaluator
from pokercard import PokerCard, POKERCARDS_SUIT_DICT, POKERCARDS_VALUE_DICT

RANK_NAMES = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]

class Calculator:
    def __init__(self, hand1: list[PokerCard], hand2: list[PokerCard]):
        self.hand1 = hand1
        self.hand2 = hand2
        self.deck = []
        self.results_all = []
        
    def initialize_deck(self):
        self.deck = []
        for suit in POKERCARDS_SUIT_DICT.keys():
            for value in POKERCARDS_VALUE_DICT.keys():
                self.deck.append(PokerCard(value, suit))

    def remove_private_cards(self):
        remaining_cards = []
        for card in self.deck:
            if not card in self.hand1 + self.hand2:
                remaining_cards.append(card)
        self.deck = remaining_cards

    @property
    def public_cards_all_combinations(self):
        return combinations(self.deck, 5)

    def compare_hands(self, public_cards):
        h1_values = HandValueEvaluator(self.hand1, list(public_cards)).determine_handvalue()
        h2_values = HandValueEvaluator(self.hand2, list(public_cards)).determine_handvalue()

        for h1_value, h2_value in zip(h1_values, h2_values):
            if h1_value > h2_value:
                return ("h1", h1_values[0], h2_values[0])
            elif h1_value < h2_value:
                return ("h2", h1_values[0], h2_values[0])
        return ("tie", h1_values[0], h2_values[0])

    def calculate(self, process_count: int):
        start = time.time()
        print(self.hand1)
        print(self.hand2)
        print("Calculating results...")
        with multiprocessing.Pool(processes=process_count) as pool:
            self.results_all = pool.map(self.compare_hands, self.public_cards_all_combinations)
    
        print(f"Duration: {round(time.time() - start, 2)}s ({round((1712304 / (time.time() - start)), 2)}it/s)")

    @staticmethod
    def _num_to_percentage(n: int):
        return round((n*100 / 1712304), 2)

    def _print_result(self, result_name: str, results: list[str], ranks: list[int] | None):
        print(f"{result_name} win rate: {round((results.count(result_name)*100 / 1712304), 2)}%")
        
        if result_name != "tie":
            ranks_counts = Counter(ranks)
            ranks_counts = list(ranks_counts.items())

            missing_ranks = set([n for n in range(1, 9)]) - set([r[0] for r in ranks_counts])

            missing_ranks = list(missing_ranks)

            if missing_ranks:
                for r in missing_ranks:
                    ranks_counts.append((r, 0))

            ranks_counts.sort(key=lambda x: x[0])

            for r, rank_name in zip(ranks_counts, RANK_NAMES):
                chance = self._num_to_percentage(r[1])
                print(f"- {rank_name: <18}{chance}% ({r[1]})")

    def display_result(self):
        results, h1_ranks, h2_ranks = zip(*self.results_all)
        
        results = list(results)
        h1_ranks = list(h1_ranks)
        h2_ranks = list(h2_ranks)
    
        self._print_result("h1", results, h1_ranks)
        self._print_result("h2", results, h2_ranks)
        self._print_result("tie", results, None)