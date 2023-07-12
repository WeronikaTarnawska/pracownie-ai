# alfa beta search - kolejność znajdywania

n = 8
inf = 999999
pos_worth = [[99, -8, 8, 6, 6, 8, -8, 99],
             [-8, -24, -4, -3, -3, -4, -24, -8],
             [8, -4, 7, 4, 4, 7, -4, 8],
             [6, -3, 4, 0, 0, 4, -3, 6],
             [6, -3, 4, 0, 0, 4, -3, 6],
             [8, -4, 7, 4, 4, 7, -4, 8],
             [-8, -24, -4, -3, -3, -4, -24, -8],
             [99, -8, 8, 6, 6, 8, -8, 99]]

me = 1
d_max = 3


def pick_move(s, my_sgn):
    possibles = s.moves_gen()
    global me, d_max
    me = my_sgn

    if not possibles:
        return ()

    elif len(possibles) == 1:
        return possibles[0]

    pss = []
    for m in possibles:
        pss.append((m, get_move_val(m, s)))
    pss.sort(reverse=True, key=lambda v: v[1])
    # print(pss)
    val = []
    for (move, h) in pss:
        s.make_move(move)
        val.append((move, min_value(s, -inf, inf, 0)))
        # print(val[-1])
        s.undo_move()
    return max(val, key=lambda v: v[1])[0]


def max_value(s, alpha, beta, d):
    if s.endgame():
        a, b = s.board_count(me, 1-me)
        return inf if a >= b else -inf
    elif d >= d_max:
        return heur_val(s)
    value = -inf
    pss = s.moves_gen()
    for m in pss:
        s.make_move(m)
        minval = min_value(s, alpha, beta, d + 1)
        s.undo_move()
        if value < minval:
            value = minval
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(s, alpha, beta, d):
    if s.endgame():
        a, b = s.board_count(me, 1-me)
        return inf if a >= b else -inf
    elif d >= d_max:
        return heur_val(s)
    value = inf
    pss = s.moves_gen()
    for m in pss:
        s.make_move(m)
        maxval = max_value(s, alpha, beta, d + 1)
        s.undo_move()
        if maxval < value:
            value = maxval
            best_move = m
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def heur_val(s):
    rund = len(s.history)
    if rund < 20:
        return pos_worth_cnt(s) + stable_disc_cnt(s) + frontier_cnt(s)
    elif rund < 56:
        return stable_disc_cnt(s) + frontier_cnt(s) + stable_pos_cnt(s)
    else:
        return gain_cnt(s) + frontier_cnt(s)


def stable_pos_cnt(s):
    val = 0
    mg = s.moves_gen()
    for m in mg:
        val += stable_pos(m, s)
    if s.cur_player == me:
        return val
    else:
        return -val


def gain_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += 1
            elif s.board[x][y] == 1-me:
                val -= 1
    return val


def frontier_cnt(s):
    front = 0
    mg = s.moves_gen()
    if s.cur_player == me:
        if len(mg) == 0:
            front -= 50
        front += len(mg)
    else:
        if len(mg) == 0:
            front += 50
        front -= len(mg)

    return front


def stable_disc_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += stable_disc((x, y), s, me)
            elif s.board[x][y] == 1-me:
                val -= stable_disc((x, y), s, 1-me)
    return val


def pos_worth_cnt(s):
    val = 0
    for x in range(n):
        for y in range(n):
            if s.board[x][y] == me:
                val += pos_worth[x][y]
            elif s.board[x][y] == 1-me:
                val -= pos_worth[x][y]
    return val


def stable_pos(m, s):
    stable = True
    xm, ym = m
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] != 1 - s.cur_player:
            stable = False
    if stable:
        return 20
    return 0


def stable_disc(m, s, player):
    x, y = m

    a, b = True, True
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

    return 60


def get_move_val(m, s):
    rund = len(s.history)
    x, y = m
    if rund < 10:
        return pos_worth[x][y]
    elif rund < 25:
        return pos_worth[x][y] + stable_disc(m, s, me) + frontier(m, s)
    elif rund < 50:
        return stable_disc(m, s, me) + frontier(m, s) + stable_pos(m, s)
    else:
        return stable_disc(m, s, me) + gain((x, y), s) + frontier(m, s) + stable_pos(m, s)


def frontier(m, s):
    xm, ym = m

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
        return 50
    return -front


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
    return result
