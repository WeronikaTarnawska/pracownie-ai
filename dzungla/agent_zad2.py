import copy
from game import *


def pick_move(possibles, s):
	me = s.player
	sss = Stan(s.player, copy.deepcopy(s.pieces), copy.deepcopy(s.board_pieces), 0)
	lim1 = 20000//len(possibles)
	vals = []
	for m in possibles:
		value = 0
		i = 0
		while i < lim1:
			ss = copy.deepcopy(sss)
			ss = make_move(m, ss)
			i += 1
			while not endgame(ss):
				ss = agent_move(moves_gen(ss), ss, pick_random)
				i += 1
			w, cs = winner(ss)
			if cs == 'player 1':
				w = 1-w
			if w == me:
				value += 1
			else:
				value -= 1
		# print(value/lim1)
		vals.append((m, value))
	return max(vals, key=lambda v: v[1])[0]
