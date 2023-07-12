import copy
from game import *


def pick_move_fast(possibles, s):
	me = s.player
	ss = Stan(s.player, copy.deepcopy(s.pieces), copy.deepcopy(s.board_pieces), 0)
	vals = []
	for m in possibles:
		new_s = copy.deepcopy(ss)
		new_s = make_move(m, new_s)
		value = eval_board(new_s, me)
		vals.append((m, value))
		# print_board(ss)
		# print((m, value))
	return max(vals, key=lambda v: v[1])[0]


def pick_move(possibles, s):
	me = s.player
	ss = Stan(s.player, copy.deepcopy(s.pieces), copy.deepcopy(s.board_pieces), 0)
	vals = []
	for m in possibles:
		new_s = copy.deepcopy(ss)
		new_s = make_move(m, new_s)
		# value = eval_board(new_s, me)
		# vals.append((m, value))
		vals.append((m, minmax(new_s, me, 0)))
		# print_board(ss)
		# print((m, value))
	return max(vals, key=lambda v: v[1])[0]


def minmax(s, me, d):
	if endgame(s):
		w, cs = winner(s)
		if cs == 'player 1' and w == me:
			return -10
		if cs == 'best piece' and w == me:
			return 200
		if cs == 'base' and w == me:
			return 1000
		else:
			return -1000
	if end_minmax(s, d):
		return eval_board(s, me)

	values = []
	ps = moves_gen(s)
	for i in ps:
		new_s = copy.deepcopy(s)
		new_s = make_move(i, new_s)
		values.append(minmax(new_s, me, d + 1))

	if not values:
		if s.player == me:
			return -100
		else:
			return 100
	if s.player == me:
		return max(values)
	else:
		return min(values)


def end_minmax(s, d):
	if d >= 2:
		return True
	if d < 2:
		return False
	ps = moves_gen(s)
	if sth_to_beat(ps, s):
		return False
	return True


def eval_board(s, me):
	my_value = 0
	op_value = 0
	eps = 0.2
	fig_val = [12, 9, 8, 7, 5, 3, 1, 10]
	my_dists = []
	op_dists = []
	for p in range(8):
		if s.pieces[me][p]:
			my_value += fig_val[p]
			my_dists.append(dist(s.pieces[me][p], den[1-me]))
		if s.pieces[1-me][p]:
			op_value += fig_val[p]
			op_dists.append(dist(s.pieces[1-me][p], den[me]))
	my_value -= min(my_dists)
	my_value -= sum(my_dists)*eps
	op_value -= min(op_dists)
	op_value -= sum(op_dists)*eps
	value = my_value - op_value
	# print(sum(my_dists), sum(op_dists))
	# print(min(my_dists), min(op_dists))
	return value


def dist(a, b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])


