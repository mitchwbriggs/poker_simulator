import holdem_engine as hldm
import hash_tools
import numpy as np
import pandas as pd
import itertools
import pickle

def build_hash_table():
    """Function that creates a Holdem Hand Evaluation Hash Lookup Table"""

    # build a deck of cards (holdem_engine.py)
    deck = hldm.Deck()

    # generate all five card poker hand combos
    combos = list(itertools.combinations(deck.cards, 5))
    num_combos = len(combos)

    # build the hash table
    hash_ids = []
    ranks = []
    subranks1 = []
    subranks2 = []
    subranks3 = []
    subranks4 = []
    subranks5 = []
    count = 0
    for combo in combos:
        count += 1

        # setup hash ids
        prime_ids = [card.prime_id for card in combo] # each card is mapped to a unique prime number
        hash_id = np.prod(np.array(prime_ids)) # prime ids are multiplied together to get unique combo ids
        hash_ids.append(hash_id)

        # build a poker hand object and evaluate it (holdem_engine.py)
        hand = hldm.Hand()
        hand.evaluate(combo)
        ranks.append(hand.rank)
        subranks1.append(hand.subranks[0])
        subranks2.append(hand.subranks[1])
        subranks3.append(hand.subranks[2])
        subranks4.append(hand.subranks[3])
        subranks5.append(hand.subranks[4])
        print(str(round(count / num_combos * 100,4)) + "% Complete")

    print("")
    print("Preparing hash table...")

    hash_dict = {'hash_id': hash_ids, 'rank': ranks, 'subrank1':subranks1,
                 'subrank2':subranks2, 'subrank3':subranks3, 'subrank4':subranks4, 'subrank5':subranks5}
    hash_df = pd.DataFrame(hash_dict)

    # sort the hash df by rank and subranks of each hand
    hash_df = hash_df.sort_values(['rank','subrank1','subrank2','subrank3','subrank4','subrank5'])

    #combine rank columns into single string values
    hash_df['combined'] = hash_df[['rank','subrank1','subrank2','subrank3','subrank4','subrank5']].apply(
                 lambda x: '_'.join(map(str, x)), axis=1)

    # assign 'univeral ranks' to each unique 'combined' rank value and write them to a new column
    hash_df['universal_rank'] = pd.factorize(hash_df.combined)[0] #pd.factorize doing the heavy lifting here

    # genarate dictionary mapping hash ids to their respective universal ranks
    hash_dict = dict(zip(hash_df['hash_id'], hash_df['universal_rank']))

    print("")
    print("Writing table to file...")

    # write hash_dict to a 'pickle' file (for efficient importing into other modules) and to a csv (for viewing/testing)
    filehandler = open('poker_hash_lookup.pickle', 'wb')
    pickle.dump(hash_dict, filehandler)
    hash_df.to_csv('poker_hash_lookup.csv', index=False)

    print("")
    print("Done!")

def get_primes():
    """ Function that returns the first 52 prime numbers in a list"""
    primes = []
    i = 1
    while len(primes) < 52:
        i += 1
        is_prime = True
        for n in range(i):
            if n+2 >= i:
                break
            else:
                if i % (n+2) == 0:
                    is_prime = False
                    break

        if is_prime is True:
            primes.append(i)

    return primes
