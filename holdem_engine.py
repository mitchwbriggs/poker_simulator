import random
import hash_tools
from collections import Counter

class Card:
    """Class representing a standard playing card.  It contains the following attributes: suit, value, ordinal, name."""
    def __init__(self, suit, value,value_plural, ordinal, card_id, prime_id, name_short):
        self.id = card_id
        self.prime_id = prime_id # for hash lookups
        self.suit = suit
        self.value = value
        self.value_plural = value_plural
        self.ordinal = ordinal
        self.name = str()
        self.create_name()
        self.name_short = name_short

    def create_name(self):
        """Method that creates the card show name by combining suit and value data into a string"""
        self.name = str(self.value + " of " + self.suit)

    def create_shorthand(self):
        """Method that creates a the shorthand card show name ('Ace of Hearts = AH) and assigns it to self"""
        self.shorthand = str()

class Deck:
    """Class representing a deck of cards.  It houses the following attributes: cards.  The class also has the following methods: draw_card, shuffle."""
    def __init__(self):
        """Contructor function that creates a list attribute 'cards' and calls the build_deck method to build the deck of cards."""
        self.cards = []
        self.build()

    def build(self):
        """Method that builds a deck of cards (where each card belongs to the class Card)."""
        self.cards = [] # clear list of cards
        suits = ["Spades", "Diamonds", "Clubs", "Hearts"]
        values = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        short_values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        values_plural = ["Twos", "Threes", "Fours", "Fives", "Sixes", "Sevens", "Eights", "Nines", "Tens", "Jacks", "Queens", "Kings", "Aces"]
        values_ordinal = [13,12,11,10,9,8,7,6,5,4,3,2,1]
        prime_ids = hash_tools.get_primes()
        id_count = 0
        for index, value in enumerate(values):
            for suit in suits:
                prime_id = prime_ids[id_count]
                id_count += 1
                suit = suit
                value = value
                value_plural = values_plural[index]
                value_ordinal = values_ordinal[index]
                name_short = short_values[index] + suit[0]
                self.cards.append(Card(suit, value, value_plural, value_ordinal, id_count, prime_id, name_short))

    def shuffle(self):
        """Method that randomly shuffles the deck."""
        random.shuffle(self.cards)

    def draw_card(self):
        """Method that draws a card from the top of the deck (first card in list representing the deck).
            The function returns the card it drew."""
        card = self.cards.pop(0)
        return card

    def burn_card(self):
        """Method that removes a card from the top of the deck (first card in the list representing the deck). The function returns nothing."""
        del self.cards[0]

    def remove_card(self, card_to_remove):
        """Method that removes a specific card from the Deck.  Takes in a list of Card objects as an input"""
        [self.cards.remove(card) for card in self.cards if card.id == card_to_remove.id]


class Player:
    """Class representing a player at the table.
        Player objects have the following attributes: name (str), stack (float), hole_cards (list)."""

    def __init__(self):
        self.name = str()
        self.stack = float()
        self.betting_pos = int()
        self.hole_cards = [] # list of Card objects
        self.available_cards = [] # hole cards + board cards
        self.hand = Hand() # Hand object
        self.range = None # Object of the type Range (defined in equity_calculator.py)

    def deal_card(self, deck):
        """Method that deals a card to the Player.  Required deck as an input (deck must be an obeject of the class 'Deck')."""
        self.hole_cards.append(deck.draw_card())

    def eval_hand(self, board_cards):
        """"Method that takes in a list of board Cards as an input and then evaluates all available Cards, creates a Hand object, and assigns it to self.hand"""
        self.available_cards = self.hole_cards + board_cards
        self.hand = Hand()
        self.hand.evaluate(self.available_cards)

    def assign_range(self, rng):
        """Method that takes in a Range object as an input and assigns it to self.range"""
        self.range = rng


class Hand:
    """Class that represents a poker hand.  Hand objects have the following attributes: evaluated (Boolean intitialized to False), cards (list of Cards), kickers (list of Cards), type (str), name (str), rank (int),
        subranks (list of ints), kickers_ordinals (list of ints)"""

    def __init__(self):
        self.evaluated = False
        self.cards = []
        self.kickers = []
        self.type = str()
        self.name = str()
        self.rank = int()
        self.subranks = []
        self.score = int()
        self.kickers_ordinals = []

    def evaluate(self, cards):
        """Method that evaluates a list of Cards (input_cards) and updates the hand object attributes accordingly"""

        evals = [self.check_straightflush_royalflush, self.check_fourofakind, self.check_fullhouse, self.check_flush,
                 self.check_straight, self.check_combos, self.assign_nohand]

        for evaluation_type in evals:
            evaluation_type(cards)
            if self.evaluated is True:
                break

    def check_straightflush_royalflush(self, cards):
        """ Method that checks for the hand type, 'Straight Flush', and assigns appropriate attributes if true.
            Uses a list of cards (Card objects) as an input. """

        card_suits = [card.suit for card in cards]
        counts = Counter(card_suits).values()
        if sum(x >= 5 for x in counts) == 1: # checking for flush
            flush_cards = [card for card in cards if card_suits.count(card.suit) >= 5]

            start = 1
            straights = []
            for _ in range(9):  # building straight combinations
                straight = [start]
                i = start
                for __ in range(4):
                    straight.append(i + 1)
                    i += 1
                start += 1
                straights.append(straight)
            straights.append([10, 11, 12, 13, 1])  # adding in ace-low straight

            flush_ordinals = [card.ordinal for card in flush_cards]
            for straight in straights:  # check for straights
                if set(straight).issubset(flush_ordinals) is True:  # if straight, build straight then break loop
                    my_straightflush = []
                    for ordinal in straight:  # build intitial my_straight list (of Cards)
                        my_straightflush += [card for card in flush_cards if card.ordinal == ordinal]

                    my_st_ordinals = [card.ordinal for card in my_straightflush]
                    for card in my_straightflush:  # keep only 5 straight cards
                        if my_st_ordinals.count(card.ordinal) > 1:
                            my_straightflush.remove(card)
                            my_st_ordinals.remove(card.ordinal)

                    if my_straightflush[0].value == "Ace": # checking for royal flush
                        self.evaluated = True
                        self.cards = my_straightflush
                        self.kickers = None
                        self.type = 'Royal Flush'
                        self.name = self.type + ' of ' + self.cards[0].suit
                        self.rank = 1
                        self.subranks = [card.ordinal for card in self.cards]
                        self.kickers_ordinals = None
                    else:
                        self.evaluated = True
                        self.cards = my_straightflush
                        self.kickers = None
                        self.type = 'Straight Flush'
                        self.name = self.type + ' of ' + self.cards[0].suit + ', ' + self.cards[0].value + ' High'
                        self.rank = 2
                        self.subranks = [card.ordinal for card in self.cards]
                        self.kickers_ordinals = None
                    break

    def check_fourofakind(self, cards):
        """Method that checks for the hand type, 'Four of a Kind', and assigns appropriate attributes if true.
            Uses a list of cards (Card objects) as an input."""

        all_card_vals = [card.value for card in cards]
        counts = Counter(all_card_vals).values()
        if sum(x == 4 for x in counts) >= 1:
            quads_cards = [card for card in cards if all_card_vals.count(card.value) == 4]
            self.evaluated = True
            self.cards = self.keep_five(cards, quads_cards)
            self.kickers = self.cards[4:]
            self.type = 'Four of a Kind'
            self.name = self.type + ', ' + self.cards[0].value_plural
            self.rank = 3
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = [card.ordinal for card in self.kickers]

    def check_fullhouse(self, cards):
        """ Method that checks for the hand type, 'Full House', and assigns appropriate attributes if true.
         Uses a list of cards (Card objects) as an input. """

        is_fh = False
        all_card_vals = [card.value for card in cards]
        counts = Counter(all_card_vals).values()
        if sum(x == 3 for x in counts) > 1:
            trips_cards = self.order_cards([card for card in cards if all_card_vals.count(card.value) == 3])
            fh_cards = trips_cards[:5]
            is_fh = True
        elif sum(x == 3 for x in counts) == 1:
            trips_cards = self.order_cards([card for card in cards if all_card_vals.count(card.value) == 3])
            if sum(x == 2 for x in counts) > 1:
                pair_cards = self.order_cards([card for card in cards if all_card_vals.count(card.value) == 2])
                fh_cards = (trips_cards + pair_cards)[:5]
                is_fh = True

        if is_fh is True:
            self.evaluated = True
            self.cards = fh_cards
            self.kickers = None
            self.type = 'Full House'
            self.name = self.type + ', ' + self.cards[0].value_plural + ' Full of ' + self.cards[3].value
            self.rank = 4
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = None

    def check_flush(self, cards):
        """ Method that checks for the hand type, 'Flush', and assigns appropriate attributes if true.
        Uses a list of cards (Card objects) as an input. """
        card_suits = [card.suit for card in cards]
        counts = Counter(card_suits).values()
        if sum(x >= 5 for x in counts) == 1:
            flush_cards = [card for card in cards if card_suits.count(card.suit) >= 5]
            self.evaluated = True
            self.cards = self.keep_five(cards, flush_cards)
            self.kickers = None
            self.type = 'Flush'
            self.name = self.type + ' of ' + self.cards[0].suit + ', ' + self.cards[0].value + ' High'
            self.rank = 5
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = None

    def check_straight(self, cards):
        """"Method that checks for the hand type, 'Straight', and assigns appropriate attributes if true. Uses a list of cards (Card objects) as an input."""
        start = 1
        straights = []
        for _ in range(9):  # building straight combinations
            straight = [start]
            i = start
            for __ in range(4):
                straight.append(i + 1)
                i += 1
            start += 1
            straights.append(straight)
        straights.append([10,11,12,13,1])  # adding in ace-low straight

        card_ordinals = [card.ordinal for card in cards]
        for straight in straights: # check for straights
            if set(straight).issubset(card_ordinals) is True: # if straight, build straight then break loop
                my_straight = []
                for ordinal in straight: #build intitial my_straight list (of Cards)
                    my_straight += [card for card in cards if card.ordinal == ordinal]

                my_st_ordinals = [card.ordinal for card in my_straight]
                for card in my_straight: # keep only 5 straight cards
                    if my_st_ordinals.count(card.ordinal) > 1:
                        my_straight.remove(card)
                        my_st_ordinals.remove(card.ordinal)

                self.evaluated = True
                self.cards = my_straight
                self.kickers = None
                self.type = 'Straight'
                self.name = self.type + ', ' + self.cards[0].value + ' High'
                self.rank = 6
                self.subranks = [card.ordinal for card in self.cards]
                self.kickers_ordinals = None
                break

    def check_combos(self, cards):
        """Function that checks for and builds a Hand object representing the type, 'Three of a Kind', 'Two Pair', or 'One Pair'.
        Uses a list of cards (Card objects) as an input."""
        all_card_vals = [card.value for card in cards]
        counts = Counter(all_card_vals).values()
        if sum(x == 3 for x in counts) >= 1:
            trips_cards = [card for card in cards if all_card_vals.count(card.value) == 3]
            self.evaluated = True
            self.cards = self.keep_five(cards, trips_cards)
            self.kickers = self.cards[3:]
            self.type = 'Three of a Kind'
            self.name = self.type + ', ' + self.cards[0].value_plural
            self.rank = 7
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = [card.ordinal for card in self.kickers]

        elif sum(x == 2 for x in counts) >= 2:
            pair_cards = [card for card in cards if all_card_vals.count(card.value) == 2]
            self.evaluated = True
            self.cards = self.keep_five(cards, pair_cards)
            self.kickers = self.cards[4:]
            self.type = 'Two Pair'
            self.name = self.type + ', ' + self.cards[0].value_plural + ' and ' + self.cards[2].value_plural
            self.rank = 8
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = [card.ordinal for card in self.kickers]

        elif sum(x == 2 for x in counts) == 1:
            pair_cards = [card for card in cards if all_card_vals.count(card.value) == 2]
            self.evaluated = True
            self.cards = self.keep_five(cards, pair_cards)
            self.kickers = self.cards[2:]
            self.type = 'One Pair'
            self.name = self.type + ' of ' + self.cards[0].value_plural
            self.rank = 9
            self.subranks = [card.ordinal for card in self.cards]
            self.kickers_ordinals = [card.ordinal for card in self.kickers]

    def assign_nohand(self, cards):
        ordered_cards = self.order_cards(cards)
        best_five = ordered_cards[:5]
        self.evaluated = True
        self.cards = best_five
        self.kickers = None
        self.type = 'High Card'
        self.name = self.type + ', ' + self.cards[0].name
        self.rank = 10
        self.subranks = [card.ordinal for card in self.cards]
        self.kickers_ordinals = None

    @staticmethod
    def keep_five(all_cards, made_cards):
        """Function that takes in a list of cards (all_cards) and a list of the cards in the set that are relevant for a made hand (made_cards) and returns up to best 5 cards."""
        first_best = Hand().order_cards(made_cards)
        next_best = Hand().order_cards([card for card in all_cards if card not in made_cards])
        five_cards = (first_best + next_best)[:5]
        return five_cards

    @staticmethod
    def order_cards(cards):
        """Function that takes in a set of cards and returns them in ordinal rank order (lowest to highest)"""
        ordered_cards = sorted(cards, key=lambda card: card.ordinal, reverse=False)
        return ordered_cards


