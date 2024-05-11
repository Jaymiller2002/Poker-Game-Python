import random

class Card:
    RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    SUITS = ("♠️", "♦️", "♥️", "♣️")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if self.deck:
            return self.deck.pop(0)
        else:
            return None

class Poker:
    def __init__(self, num_hands, player_names):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = [self.deal_hand() for _ in range(num_hands)]
        self.tlist = []
        self.player_names = player_names

    def deal_hand(self):
        return [self.deck.deal() for _ in range(5)]

    def play(self):
        for player_name, hand in zip(self.player_names, self.hands):
            sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
            print(f"\033[36m{player_name}: {' '.join(map(str, sorted_hand))}\033[0m")
            print("")  # Add an empty print statement for space between hands

    def calculate_point(self, hand):
        sorted_hand = sorted(hand, key=lambda card: Card.RANKS.index(card.rank), reverse=True)
        return sum(Card.RANKS.index(card.rank) * (13 ** (4 - i)) for i, card in enumerate(sorted_hand))

    def is_royal_flush(self, hand):
        suits = set(card.suit for card in hand)
        if len(suits) == 1:
            ranks = sorted(card.rank for card in hand)
            if ranks == ['10', 'J', 'Q', 'K', 'A']:
                print("Royal Flush")
                return True
        return False

    def is_straight_flush(self, hand):
        suits = set(card.suit for card in hand)
        if len(suits) == 1:
            ranks = sorted(Card.RANKS.index(card.rank) for card in hand)
            if max(ranks) - min(ranks) == 4:
                print("Straight Flush")
                return True
        return False

    def is_four_of_a_kind(self, hand):
        ranks = [card.rank for card in hand]
        for rank in ranks:
            if ranks.count(rank) == 4:
                print("Four of a Kind")
                return True
        return False

    def is_full_house(self, hand):
        ranks = [card.rank for card in hand]
        if len(set(ranks)) == 2 and (ranks.count(ranks[0]) == 3 or ranks.count(ranks[0]) == 2):
            print("Full House")
            return True
        return False

    def is_flush(self, hand):
        suits = set(card.suit for card in hand)
        if len(suits) == 1:
            print("Flush")
            return True
        return False

    def is_straight(self, hand):
        ranks = sorted(Card.RANKS.index(card.rank) for card in hand)
        if max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5:
            print("Straight")
            return True
        return False

    def is_three_of_a_kind(self, hand):
        ranks = [card.rank for card in hand]
        for rank in ranks:
            if ranks.count(rank) == 3:
                print("Three of a Kind")
                return True
        return False

    def is_two_pair(self, hand):
        ranks = [card.rank for card in hand]
        pair_ranks = [rank for rank in set(ranks) if ranks.count(rank) == 2]
        if len(pair_ranks) == 2:
            print("Two Pair")
            return True
        return False

    def is_one_pair(self, hand):
        ranks = [card.rank for card in hand]
        for rank in ranks:
            if ranks.count(rank) == 2:
                print("One Pair")
                return True
        return False

    def is_high_card(self, hand):
        print("High Card")
        return True

    def determine_winner(self):
        for i, hand in enumerate(self.hands):
            if self.is_royal_flush(hand):
                self.tlist.append((i, 10 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_straight_flush(hand):
                self.tlist.append((i, 9 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_four_of_a_kind(hand):
                self.tlist.append((i, 8 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_full_house(hand):
                self.tlist.append((i, 7 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_flush(hand):
                self.tlist.append((i, 6 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_straight(hand):
                self.tlist.append((i, 5 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_three_of_a_kind(hand):
                self.tlist.append((i, 4 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_two_pair(hand):
                self.tlist.append((i, 3 * (13 ** 5) + self.calculate_point(hand)))
            elif self.is_one_pair(hand):
                self.tlist.append((i, 2 * (13 ** 5) + self.calculate_point(hand)))
            else:
                self.tlist.append((i, 1 * (13 ** 5) + self.calculate_point(hand)))

        winner_index = max(self.tlist, key=lambda x: x[1])[0]
        print(f"\n\033[32m{self.player_names[winner_index]} wins.\033[0m")
        print("")  # Add an empty print statement for space after winner announcement

def main():
    while True:
        num_hands = int(input("\033[32mEnter number of hands to play: \033[0m"))
        while num_hands < 1 or num_hands > 10:
            num_hands = int(input("\033[32mEnter number of hands to play (2-6): \033[0m"))
        player_names = [input(f"\033[32mEnter name for Player {i + 1}: \033[0m") for i in range(num_hands)]
        game = Poker(num_hands, player_names)
        game.play()
        game.determine_winner()

        play_again = input("\033[34mDo you want to play again? (yes/no): \033[0m").lower()
        if play_again != "yes":
            break
        print("")  # Add an empty print statement for space between games

if __name__ == "__main__":
    main()