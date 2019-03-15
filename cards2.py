# https://realpython.com/python-logging/
from loggy.clscards import ClassCards
import time

Cards = ClassCards()
Cards.configure_logger()

stats = dict.fromkeys(['p1', 'p2', 'tie'], 0)

start = time.time()
for games in range(10000):
    win = Cards.war()
    # print(win)
    stats[win] += 1
end = time.time()
print('elapsed time = ', end - start)
print(stats)

