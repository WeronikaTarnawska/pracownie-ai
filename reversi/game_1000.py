import copy

import random_agent as agent0
import reversi_fast as agent1
from game import Game 
import time


def my_copy(xs):
    return [[xs[i][j] for j in range(len(xs[0]))] for i in range((len(xs)))]


moves_t = [0, 0]
moves_num = [0, 0]
my_score, his_score = 0, 0
me = 1
pick = (agent0.pick_move, agent1.pick_move)
# zawsze zaczyna 0
for _ in range(1000):
    # print(_)
    s = Game(True)
    player = 0
    while True:
        f = pick[player]
        ta = time.perf_counter()
        m = f(s, player)
        tb = time.perf_counter()
        moves_t[player] += tb - ta
        moves_num[player] += 1

        s.make_move(m)
        if s.endgame():
            r = s.board_count(me, 1-me)
            if r[0] > r[1]:
                my_score += 1
            elif r[0] < r[1]:
                his_score += 1
            break
        player = 1-player
    me = 1-me
    pick = (pick[1], pick[0])

print(f"my score: {my_score}")
print(f"his score: {his_score}")
print(f"draws: {1000-my_score-his_score}")
print(f"{'level 3 (standard)' if his_score < 20 else 'level 2 (basic)' if his_score < 70 else 'level 1 (novi)' if his_score < 200 else 'przegraliśmy :('}")
print(f'efficiency {round((my_score/(my_score+his_score))*100)}%')
print(f'average move time for agent 0: {moves_t[0]/moves_num[0]}')
print(f'average move time for agent 1: {moves_t[1]/moves_num[1]}')
print(f"time: {time.process_time()} seconds")


