import holdem_engine as hldm

#TESTING HOLDEM_ENGINE HAND EVALUATION

count = 0
desired = False
while desired is False:
    count += 1

    deck = hldm.Deck()
    deck.shuffle()

    set_of_cards = deck.cards[:7]
    print("My cards:", [card.name for card in set_of_cards])

    hand = hldm.Hand()
    hand.evaluate(set_of_cards)
    print("My hand:", [card.name for card in hand.cards])
    print("Hand Type:",hand.type)
    print("Hand Name:",hand.name)
    print("Hand Rank, Card Ranks:", str(hand.rank) + ",", hand.subranks)
    try:
        print("Kickers:", [card.display_name for card in hand.kickers])
        print("Kickers_ordinals:", [ordinal for ordinal in hand.kickers_ordinals])
    except:
        pass
    print("")

    if hand.type == 'Straight Flush':
        desired = True
        print("Hand type, '" + hand.type + "', occurred after " + str(count) + " hands.")


