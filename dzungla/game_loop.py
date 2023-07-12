import copy
import time

from game import *
import agent_zad2
import agent_zad3


def game_loop(n, agent, name):
    t1 = time.perf_counter()
    me = 1
    ile = 0
    for r in range(n):
        stan = Stan(r % 2, [copy.deepcopy(player_0_start), copy.deepcopy(player_1_start)], copy.deepcopy(bd0), 0)
        itr = 0
        while True:
            itr += 1
            possibl = moves_gen(stan)
            #print(possibl)
            stan = agent_move(possibl, stan, agent[stan.player])
            #print_board(stan)
            if endgame(stan):
                # print_board(stan)
                print(itr)
                #print(winner(stan))
                w, cs = winner(stan)
                if cs == 'player 1':
                    w = (r+1)%2
                if w == me:
                    ile += 1
                    print(':)')
                break
    t2 = time.perf_counter()
    print(f'{name[me]} winning %: {ile/n}')
    print(f'{name[1-me]} winning %: {1 - (ile / n)}')
    print('time: ', t2-t1)
    print()


n = 10
game_loop(n, [agent_zad2.pick_move, agent_zad3.pick_move], ['zad2', 'zad3'])
#game_loop(n, [agent_zad2.pick_move, agent_zad3.pick_move_fast], ['zad2', 'zad3 bez minmaxa'])
#game_loop(n, [pick_random, agent_zad3.pick_move], ['rand', 'zad3'])
#game_loop(n, [pick_random, agent_zad3.pick_move_fast], ['rand', 'zad3 bez minmaxa'])
#game_loop(n, [pick_random, agent_zad2.pick_move], ['rand', 'zad2'])
#game_loop(n, [pick_random, pick_random], ['rand', 'rand'])
#game_loop(n, [agent_zad3.pick_move_fast, agent_zad3.pick_move_fast], ['zad3 bez minmaxa', 'zad3 bez minmaxa'])
#game_loop(n, [agent_zad2.pick_move, agent_zad2.pick_move], ['zad2', 'zad2'])
