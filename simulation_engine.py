import holdem_engine as hldm
from functools import reduce
import itertools
import random
import pickle


class Simulation:
    """Class that represents a Poker simulation"""
    def __init__(self, scenario):
        self.scenario = scenario # object of type Scenario
        self.result = None # object of type Results
        with open('hash_lookup.pickle', 'rb') as handle:
            self.lookup_score = pickle.load(handle) # eval hash table (type dict)

    def run(self):
        """Method that runs simulations and returns estimated win probability"""
        count = total_wins = total_ties = 0
        num_rounds = 15*1000

        deck = hldm.Deck()
        prime_map = dict()
        for card in deck.cards:
            prime_map[card.prime_id] = card

        user = self.scenario.user
        user_cards = user.hole_cards
        board_cards = self.scenario.board_cards

        user_primes = [card.prime_id for card in user_cards]
        board_primes = [card.prime_id for card in board_cards]

        length_board = len(board_cards)
        length_hole = len(user_cards)
        num_missing_board = 5 - length_board
        num_missing_user = 2 - length_hole

        burnt_primes = user_primes + board_primes
        avbl_primes = [card.prime_id for card in deck.cards if card.prime_id not in burnt_primes]

        opponents = self.scenario.opponents
        num_opponents = len(opponents)
        num_primes = num_missing_user + num_missing_board + (num_opponents * 2)
        for _ in range(num_rounds):
            count += 1

            rndm_primes = random.sample(avbl_primes, num_primes)
            user_primes_full = user_primes + rndm_primes[:num_missing_user]
            board_primes_full = board_primes + rndm_primes[num_missing_user:num_missing_board]
            user_score = self.get_score(user_primes_full, board_primes_full)

            num_beaten = 0
            num_tied = 0
            start_index = num_missing_board + num_missing_user
            for __ in range(num_opponents):
                end_index = start_index + 2
                opp_primes = rndm_primes[start_index:end_index]
                start_index += 2
                opp_score = self.get_score(board_primes_full, opp_primes)
                if opp_score < user_score:
                    pass
                elif opp_score == user_score:
                    num_tied += 1
                else:
                    num_beaten += 1

            if num_beaten == num_opponents:
                total_wins += 1
            elif num_tied == num_opponents:
                total_ties += 1

        self.result = str(round(total_wins / count * 100)) + '%'

    def get_score(self, board_primes, hole_primes):
        """ Method that takes in Board Card IDs (list) and Hole Card IDs (list) and returns a hand score (int)"""

        #list of the 7 cards that are available to the player (board cards + hole cards)
        avbl_ids = board_primes + hole_primes

        #generate all possible 5 card combinations from avbl_ids
        combos = itertools.combinations(avbl_ids, 5)

        # lookup all card combos in the hand score hash table (from hash_tools.py) and return the best score (lowest)
        score = min([self.lookup_score[reduce(lambda x, y: x * y, id_list)] for id_list in combos])

        return score


class Scenario:
    """Class that serves as a container for simulation conditions"""

    def __init__(self, user, opponents, board_cards):
        self.user = user # Player object (Player objects defined in holdem_engine.py)
        self.opponents = opponents # list of Player objects (Player objects defined in holdem_engine.py)
        self.board_cards = board_cards # list of cards on board (Card objects defined in holdem_engine.py)

