# monte carlo tree search do zadania 1 z p4
# (do zadania 5 z p4 tylko zmienić parametry)

from collections import namedtuple
import copy
import math
import random
from game import Game


class Node:
    def __init__(self, m, t, n, k, d):
        self.last_move = m
        self.score = t
        self.visits = n
        self.kids = k
        self.dad = d


me = 1
games_per_roll = 2
mcts_iterations = 2
magical_const = 2
infinity = 999999
# do zad5 p4 (ruch 0.5 s):
# games_per_roll, mcts_iterations = 16, 10
# + len(state.history)

# do game_1000 - zad1 p4 standard:
# games_per_roll, mcts_iterations = 2, 2
# + len(state.history)//4


def pick_move(state, my_sgn):
    global me
    me = my_sgn
    s = state.copy_game()
    tree = Node((), 0, 0, [], None)
    expand(tree, s)
    for k in tree.kids:
        k.score = get_move_val(k.last_move, s)
    to_undo = 0
    for n in range(mcts_iterations + len(state.history)//8):
        cur = tree
        while cur.kids:
            vals = [(ucb(k, n), k) for k in cur.kids]
            cur = max(vals, key=lambda v: v[0])[1]
            s.make_move(cur.last_move)
            to_undo += 1
        if cur.visits != 0:
            expand(cur, s)
            if cur.kids:
                cur = random.choice(cur.kids)
                s.make_move(cur.last_move)
                to_undo += 1
        score = rollout(cur, s)
        backpr(score, cur)
        for _ in range(to_undo):
            s.undo_move()
        to_undo = 0
    t = []
    for k in tree.kids:
        if k.visits != 0 and k.last_move:
            t.append((k.score / k.visits, k.last_move))
        elif k.visits == 0 and k.last_move:
            t.append((-infinity, k.last_move))
    if t:
        return max(t, key=lambda v: v[0])[1]
    else:
        return ()


def backpr(scr, node):
    while node.dad:
        node.score += scr
        node.visits += 1
        node = node.dad


def expand(node, state):
    possibles = state.moves_gen()
    if not possibles:
        node.kids.append(Node((), 0, 0, [], node))
        return
    for m in possibles:
        node.kids.append(Node(m, 0, 0, [], node))


def ucb(node, n):
    if node.visits == 0:
        return infinity+node.score
    return node.score / node.visits + magical_const * math.sqrt(math.log2(n) / node.visits)


def rollout(node, state):
    score = 0
    for _ in range(games_per_roll):
        s = state.copy_game()
        while True:
            mg = s.moves_gen()
            if mg:
                s.make_move(random.choice(mg))
            else:
                s.make_move(())
            if s.endgame():
                a, b = s.board_count(me, 1 - me)
                if a > b:
                    score += 1
                elif b > a:
                    score -= 1
                break
    return score


def stable_disc(m, s, player):
    if not m:
        return 0
    x, y = m
    a, b = True, True
    n = 8
    for i in range(1, min(x, y) + 1):
        if s.board[x - i][y - i] != player:
            a = False
            break
    for i in range(1, min(n - x, n - y)):
        if s.board[x + i][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, min(n - 1 - x, y) + 1):
        if s.board[x + i][y - i] != player:
            a = False
            break
    for i in range(1, min(x, n - 1 - y) + 1):
        if s.board[x - i][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, x + 1):
        if s.board[x - i][y] != player:
            a = False
            break
    for i in range(1, n - x):
        if s.board[x + i][y] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, y + 1):
        if s.board[x][y - i] != player:
            a = False
            break
    for i in range(1, n - y):
        if s.board[x][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0
    return 2


def get_move_val(m, s):
    rund = len(s.history)
    if not m:
        return -infinity
    x, y = m
    if rund < 10:
        return pos_worth[x][y]/100
    elif rund < 25:
        return pos_worth[x][y]/100 + stable_disc(m, s, me) + frontier(m, s)
    elif rund < 48:
        return stable_disc(m, s, me) + frontier(m, s) + stable_pos(m, s)
    elif rund < 56:
        return stable_disc(m, s, me) + gain((x, y), s) + frontier(m, s) + stable_pos(m, s)
    else:
        return 0


def frontier(m, s):
    xm, ym = m
    n = 8
    mine = [[False for _ in range(n)] for _ in range(n)]
    flipped = []
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        to_flip = []
        while 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == 1-me:
            to_flip.append((x, y))
            x += dx
            y += dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == me:
            flipped += to_flip
            for (i, j) in to_flip:
                mine[i][j] = True

    flipped.append(m)
    mine[xm][ym] = True

    front = 0
    for (px, py) in s.free:
        if mine[px][py]:
            continue
        for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            x, y, i = px + dx, py + dy, 0
            while 0 <= x < n and 0 <= y < n and (s.board[x][y] == me or mine[x][y]):
                x += dx
                y += dy
                i += 1
            if 0 <= x < n and 0 <= y < n and i > 0 and s.board[x][y] == 1-me:
                front += 1
                break

    if front == 0:
        return 2
    return -front/100


def gain(m, s):
    xm, ym = m
    result = 0
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        to_flip = 0
        while 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == 1-me:
            to_flip += 1
            x += dx
            y += dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == me:
            result += to_flip
    # print(m, result)
    return result/200


def stable_pos(m, s):
    stable = True
    xm, ym = m
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] != 1-me:
            stable = False
    if stable:
        return -1
    return 0


pos_worth = [[99, -8, 8, 6, 6, 8, -8, 99],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [99, -8, 8, 6, 6, 8, -8, 99]]
