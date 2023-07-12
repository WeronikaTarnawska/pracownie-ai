# tylko heura
# 2. Poziom basic: na 1000 gier co najwyżej 70 porażek (czas działania całego eksperymentu mniej niż 1 minuta)

# "pos worth" - to na początku: pozycje lepsze i gorsze
# "stable disc" - kładź tak, żeby już nie można było ich flipnąć
# "mobility" - dużo możliwości w kolejnym ruch (jak to liczyć?? ... )
# "evaporation" - mało moich na początku, bo to mniej możliwości dla przeciwnika (odejmij gain, zamiast dodawać?)
# "frontier" - mało zewnętrznych, takich, które umożliwiają ruch przeciwnikowi
# "stable pos" - dziura w strefie przeciwnika, on już tam nie postawi nigdy, więc można takie miejsce zachować na ostatni ruch
import copy
from game import Game
import random
n = 8

pos_worth = [[99, -8, 8, 6, 6, 8, -8, 99],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [6, -3, 4, 0, 0, 4, -3, 6],
        [8, -4, 7, 4, 4, 7, -4, 8],
        [-8, -24, -4, -3, -3, -4, -24, -8],
        [99, -8, 8, 6, 6, 8, -8, 99]]

me, him = 1, 0


def pick_move(s, my_sgn):
    possibles = s.moves_gen()
    global me, him
    if my_sgn == 0:
        me, him = him, me

    if not possibles:
        return ()

    elif len(possibles) == 1:
        return possibles[0]

    val = []
    for m in possibles:
        val.append((m, get_move_val(m, s)))

    upwd = []
    for v in val:
        if v[1] > 100:
            upwd.append(v)

    if len(upwd) > 1:
        return random.choice(upwd)[0]
    elif len(upwd) == 1:
        return upwd[0][0]
    else:
        return max(val, key=lambda vi: vi[1])[0]


def get_move_val(m, s):
    rund = len(s.history)
    x, y = m
    if rund < 10:
        return pos_worth[x][y]
    elif rund < 25:
        return pos_worth[x][y] + stable_disc(m, s, me) + frontier(m, s)*2
    elif rund < 48:
        return stable_disc(m, s, me) + frontier(m, s)*2 + stable_pos(m, s)
    elif rund < 56:
        return stable_disc(m, s, me) + gain((x, y), s) + frontier(m, s)*2 + stable_pos(m, s)
    else:
        return gain((x, y), s) + frontier(m, s)*2


def frontier(m, s):
    xm, ym = m

    mine = [[False for _ in range(n)] for _ in range(n)]
    flipped = []
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        to_flip = []
        while 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == him:
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
            if 0 <= x < n and 0 <= y < n and i > 0 and s.board[x][y] == him:
                front += 1
                break

    if front == 0:
        return 150
    return -front


def gain(m, s):
    xm, ym = m
    result = 0
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        to_flip = 0
        while 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == him:
            to_flip += 1
            x += dx
            y += dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] == me:
            result += to_flip
    # print(m, result)
    return result


def stable_pos(m, s):
    stable = True
    xm, ym = m
    for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = xm + dx, ym + dy
        if 0 <= x < s.n and 0 <= y < s.n and s.board[x][y] != him:
            stable = False
    if stable:
        return -140
    return 0


def stable_disc(m, s, player):
    x, y = m

    a, b = True, True
    for i in range(1, min(x, y)+1):
        if s.board[x - i][y - i] != player:
            a = False
            break
    for i in range(1, min(n-x, n-y)):
        if s.board[x + i][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, min(n-1-x, y) + 1):
        if s.board[x + i][y - i] != player:
            a = False
            break
    for i in range(1, min(x, n-1-y) + 1):
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
    for i in range(1, n-x):
        if s.board[x + i][y] != player:
            b = False
            break
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, y+1):
        if s.board[x][y - i] != player:
            a = False
            break
    for i in range(1, n-y):
        if s.board[x][y + i] != player:
            b = False
            break
    if not a and not b:
        return 0

    return 120


"""
stable = [[False for _ in range(8)] for _ in range(8)]
stable[0][0] = True
stable[7][7] = True
stable[0][7] = True
stable[7][0] = True


def stable_disc(m, s, player):
    x, y = m

    a, b = True, True
    for i in range(1, min(x, y)+1):
        if not stable[x - i][y - i]:
            a = False
    for i in range(1, min(n-x, n-y)):
        if not stable[x + i][y + i]:
            b = False
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, min(n-1-x, y) + 1):
        if not stable[x + i][y - i]:
            a = False
    for i in range(1, min(x, n-1-y) + 1):
        if not stable[x - i][y + i]:
            b = False
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, x + 1):
        if not stable[x - i][y]:
            a = False
    for i in range(1, n-x):
        if not stable[x + i][y]:
            b = False
    if not a and not b:
        return 0

    a, b = True, True
    for i in range(1, y+1):
        if not stable[x][y - i]:
            a = False
    for i in range(1, n-y):
        if not stable[x][y + i]:
            b = False
    if not a and not b:
        return 0

    stable[x][y] = True
    # printtab(stable)
    return 140
"""


def my_copy(xs):
    return [[xs[i][j] for j in range(len(xs[0]))] for i in range((len(xs)))]


def printtab(t):
    for l in t:
        for i in l:
            if i:
                print('$', end="")
            else:
                print('.', end="")
        print()
    print()
