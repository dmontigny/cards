# https://www.patricksoftwareblog.com/python-logging-example/
# https://realpython.com/python-itertools/

import logging
from os import path, remove
import itertools as it


class ClassCards(object):
    def __init__(self):
        import sys
        self.current_number = 0
        self.logname = path.basename(sys.argv[0][:-3]) + '.log'
        self.ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.suits = ['♠', '♦', '♥', '♣']
        self.cards = None
        self.logger = None

    def get_cards(self):
        self.logger.debug('instantiating card deck')
        self.cards = list(it.product(self.ranks, self.suits))
        # self.logger.debug(self.cards) # no output
        return self.cards

    def shuffle(self):
        self.logger.debug('shuffling card deck')
        import random
        # self.logger.debug(type(self.cards), 'to shuffle ', self.cards)
        """Return iterator over shuffled deck."""
        self.cards = list(self.cards)
        random.shuffle(self.cards)
        # self.logger.debug(self.cards) # no output
        return iter(tuple(self.cards))

    def cut(self, n):
        self.logger.debug('cutting card deck')
        """Return an iterator over a deck of cards cut at index `n`."""
        deck1, deck2 = it.tee(self.cards, 2)
        top = it.islice(deck1, n)
        bottom = it.islice(deck2, n, None)
        return it.chain(bottom, top)

    def deal(self, numhands=2, handsize=5):
        self.logger.debug('dealing card deck')
        iters = [iter(self.cards)] * handsize
        return tuple(zip(*(tuple(it.islice(itr, numhands)) for itr in iters)))

    def war(self):
        from random import randrange
        self.logger.debug('Time for War!!')
        p1 = p2 = tie = 0
        self.cards = self.get_cards()
        # self.logger.debug(self.cards) # doesn't work
        self.cards = self.shuffle()
        self.cards = self.cut(randrange(51))
        self.cards = self.deal(2, 26)

        # lg.info(len(tuple(warcards)), list(warcards)) # should be no cards left

        self.logger.debug('starting war game')
        for card in range(len(self.cards[0])):
            # self.logger.info(''.join(self.cards[0][card]), ' vs ', ''.join(self.cards[1][card]))
            if self.ranks.index(self.cards[0][card][0]) + 2 > self.ranks.index(self.cards[1][card][0]) + 2:
                p1 += 1
                self.logger.debug('P1 wins round!')
            elif self.ranks.index(self.cards[1][card][0]) + 2 > self.ranks.index(self.cards[0][card][0]) + 2:
                p2 += 1
                self.logger.debug('P2 wins round!')
            else:
                tie += 1
                self.logger.debug('Tie round, no winner')
        self.logger.info('Scores: P1 = {}, P2 = {}, Ties = {}'.format(p1, p2, tie))
        if p1 > p2:
            self.logger.debug('P1 wins game!')
            return 'p1'
        elif p2 > p1:
            self.logger.debug('P2 wins game!')
            return 'p2'
        else:
            self.logger.debug('Tie game, no winner')
            return 'tie'

    def configure_logger(self):
        # If applicable, delete the existing log file as it is overwritten each time
        if path.isfile(self.logname):
            remove(self.logname)

        # Create the Logger
        self.logger = logging.getLogger(self.logname[:-4])
        self.logger.setLevel(logging.INFO)

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler(self.logname)
        logger_handler.setLevel(logging.INFO)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        self.logger.info('Completed configure_logger()!')
