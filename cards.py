# https://realpython.com/python-itertools/

import itertools as it

# https://realpython.com/python-logging/
import logging as lg

from random import randrange
import sys
import os
import time

# print(os.path.basename(sys.argv[0][:-3])) # get current filename

lg.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                        filename=f"{os.path.basename(sys.argv[0][:-3])}.log'",
                        filemode='a')


lg.warning('Starting cards')
lg.info('This will get logged')


ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['♠', '♦', '♥', '♣']
# suits = ['H', 'D', 'C', 'S']


def get_cards():
    cards = list(it.product(ranks, suits))

    lg.info(type(cards), 'cards: ', cards)

    cards = shuffle(cards)
    cards = cut(cards, randrange(51))
    return cards


def shuffle(deck):
    import random
    lg.info(type(deck), 'to shuffle ', deck)
    """Return iterator over shuffled deck."""
    deck = list(deck)
    random.shuffle(deck)
    return iter(tuple(deck))


def cut(deck, n):
    """Return an iterator over a deck of cards cut at index `n`."""
    deck1, deck2 = it.tee(deck, 2)
    top = it.islice(deck1, n)
    bottom = it.islice(deck2, n, None)
    return it.chain(bottom, top)


def deal(deck, numhands=2, handsize=5):
    iters = [iter(deck)] * handsize
    return tuple(zip(*(tuple(it.islice(itr, numhands)) for itr in iters)))


def war():
    lg.info('Time for war!!')
    p1 = p2 = tie = 0
    warcards = get_cards()
    warcards = deal(warcards, 2, 26)
    # print(warcards)
    lg.info(len(tuple(warcards)), list(warcards))  # should be no cards left

    for card in range(len(warcards[0])):
        lg.info(''.join(warcards[0][card]), ' vs ', ''.join(warcards[1][card]))
        if ranks.index(warcards[0][card][0]) + 2 > ranks.index(warcards[1][card][0]) + 2:
            p1 += 1
            lg.info('P1 wins round!')
        elif ranks.index(warcards[1][card][0]) + 2 > ranks.index(warcards[0][card][0]) + 2:
            p2 += 1
            lg.info('P2 wins round!')
        else:
            tie += 1
            lg.info('Tie game, no winner')
    lg.info(f"Scores: P1 = {p1}, P2 = {p2}, Ties = {tie}")
    if p1 > p2:
        lg.info('P1 wins game!')
        return 'p1'
    elif p2 > p1:
        lg.info('P2 wins game!')
        return 'p2'
    else:
        lg.info('Tie game, no winner')
    return 'tie'


stats = dict.fromkeys(['p1', 'p2', 'tie'], 0)

start = time.time()
for games in range(10000):
    win = war()
    # print(win)
    stats[win] += 1
end = time.time()
print('elapsed time = ', end - start)

print(stats)


