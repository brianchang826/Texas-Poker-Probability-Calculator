from pokercard import PokerCard
from calculator import Calculator

def main():
    # example usage
    hand1 = [PokerCard("K", "Spades"), PokerCard("K", "Hearts")]
    hand2 = [PokerCard("A", "Clubs"), PokerCard("K", "Clubs")]
    calc = Calculator(hand1, hand2)
    calc.initialize_deck()
    calc.remove_private_cards()
    calc.calculate(process_count=20)
    calc.display_result()

if __name__ == "__main__":
    main()