import copy
import random
from collections import namedtuple

board_width = 7
board_height = 9

board = [['.', '.', '#', '*', '#', '.', '.'],
         ['.', '.', '.', '#', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '~', '~', '.', '~', '~', '.'],
         ['.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '#', '.', '.', '.'],
         ['.', '.', '#', '*', '#', '.', '.']]

bd0 = [['L', '.', '.', '.', '.', '.', 'T'],
       ['.', 'D', '.', '.', '.', 'C', '.'],
       ['R', '.', 'J', '.', 'W', '.', 'E'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['.', '.', '.', '.', '.', '.', '.'],
       ['e', '.', 'w', '.', 'j', '.', 'r'],
       ['.', 'c', '.', '.', '.', 'd', '.'],
       ['t', '.', '.', '.', '.', '.', 'l']]

Stan = namedtuple('Stan', [
    'player', 'pieces', 'board_pieces', 'no_beats'
])
# e = ('.', '#', '*', '~', 'E', 'L', 'T', 'J', 'W', 'D', 'C', 'R')
piece_num = {'E':0, 'L':1, 'T':2, 'J':3, 'W':4, 'D':5, 'C':6, 'R':7,
             'e':0, 'l':1, 't':2, 'j':3, 'w':4, 'd':5, 'c':6, 'r':7}
piece_letter = [['E', 'L', 'T', 'J', 'W', 'D', 'C', 'R'], ['e', 'l', 't', 'j', 'w', 'd', 'c', 'r']]
P = namedtuple('P', ['E', 'L', 'T', 'J', 'W', 'D', 'C', 'R'])
elephant, lion, tiger, panther, wolf, dog, cat, rat = 0, 1, 2, 3, 4, 5, 6, 7
den = [(0, 3), (8, 3)]
player_0_start = [(2, 6), (0, 0), (0, 6), (2, 2), (2, 4), (1, 1), (1, 5), (2, 0)]  # 0 na górze
player_1_start = [(6, 0), (8, 6), (8, 0), (6, 4), (6, 2), (7, 5), (7, 1), (6, 6)]  # 1 na dole


def moves_gen(s):
    moves = []
    for p in range(8):
        if not s.pieces[s.player][p]:
            continue
        for m in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            newp = (s.pieces[s.player][p][0] + m[0], s.pieces[s.player][p][1] + m[1])
            if valid_move(p, s.pieces[s.player][p], newp, s):
                moves.append((p, s.pieces[s.player][p], newp))
    for p in (lion, tiger):
        if not s.pieces[s.player][p]:
            continue
        for m in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x = jump(p, s.pieces[s.player][p], m, s)
            if x:
                moves.append((p, s.pieces[s.player][p], x))
    return moves


def valid_move(piece, prev_pos, new_pos, s):
    nx, ny = new_pos
    if not (0 <= nx < board_height and 0 <= ny < board_width):
        return False
    if is_mine(s.board_pieces[nx][ny], s.player):
        return False
    if new_pos == den[s.player]:
        return False
    if board[nx][ny] == '~' and piece != rat:
        return False
    if is_enemy(s.board_pieces[nx][ny], s.player) and not can_beat(s.board_pieces[nx][ny], piece, s.player, prev_pos, new_pos):
        return False
    return True


def is_mine(sgn, player):
    if sgn == '.':
        return False
    if player == 0:
        return sgn.isupper()
    else:
        return sgn.islower()


def is_enemy(sgn, player):
    if sgn == '.':
        return False
    if player == 0:
        return sgn.islower()
    else:
        return sgn.isupper()


def can_beat(sgn, piece, player, prev_pos, new_pos):
    if not is_enemy(sgn, player):
        return False
    if board[new_pos[0]][new_pos[1]] == '#':
        return True
    if piece == rat:
        if board[prev_pos[0]][prev_pos[1]] == '~' and board[new_pos[0]][new_pos[1]] != '~':
            return False
        if piece_num[sgn] == elephant:
            return True
    if piece == elephant:
        if piece_num[sgn] == rat:
            return False
    if piece_num[sgn] >= piece:
        return True
    return False


def sth_to_beat(ps, s):
    for m in ps:
        piece, prev, newp = m
        nx, ny = newp
        if can_beat(s.board_pieces[nx][ny], piece, s.player, prev, newp):
            return True
    return False


def jump(piece, pos, move, s):
    dx, dy = move[0], move[1]
    nx, ny = pos[0] + dx, pos[1] + dy
    if not (0 <= nx < board_height and 0 <= ny < board_width):
        return False
    if board[nx][ny] != '~':
        return False
    while board[nx][ny] == '~':
        if s.board_pieces[nx][ny].lower() == 'r' and is_enemy(s.board_pieces[nx][ny], s.player):
            return False
        nx += dx
        ny += dy
    if valid_move(piece, pos, (nx, ny), s):
        return nx, ny
    return False


def make_move(m, s):
    piece, prev, newp = m
    nx, ny = newp
    player, pieces, board_pieces, no_beats = s
    if can_beat(board_pieces[nx][ny], piece, player, prev, newp):
        pieces[1-player][piece_num[board_pieces[nx][ny]]] = ()
        no_beats = 0
    else:
        no_beats += 1
    board_pieces[prev[0]][prev[1]] = '.'
    board_pieces[nx][ny] = piece_letter[player][piece]
    pieces[player][piece] = newp
    return Stan(1-player, pieces, board_pieces, no_beats)


def print_board(s):
    print(f'player = {s.player}, last beat {s.no_beats} ago')
    for line in s.board_pieces:
        for i in line:
            print(i, end="")
        print()


def endgame(s):
    # print(s.no_beats)
    if s.board_pieces[den[0][0]][den[0][1]] != '.' or s.board_pieces[den[1][0]][den[1][1]] != '.':
        # print(':)')
        return True
    if s.no_beats >= 30:
        return True
    o = True
    for p in (0, 1):
        for i in s.pieces[p]:
            if i:
                o = False
                break
    return o


def agent_move(possibles, s, pick):
    if possibles:
        m = pick(possibles, s)
        return make_move(m, s)
    return Stan(1-s.player, s.pieces, s.board_pieces, s.no_beats)


def pick_random(possibles, s):
    return random.choice(possibles)


def winner(s):
    if s.board_pieces[den[0][0]][den[0][1]] != '.':
        # print('base 1')
        return 1, 'base'
    if s.board_pieces[den[1][0]][den[1][1]] != '.':
        # print('base 0')
        return 0, 'base'
    for i in range(8):
        if s.pieces[0][i] and not s.pieces[1][i]:
            return 0, 'best piece'
        if s.pieces[1][i] and not s.pieces[0][i]:
            return 1, 'best piece'
    return 1, 'player 1'


# Obowiązują następujące zasady ruchów:
# • Gracz nie może wchodzić do własnej jamy.
# • Jedynie szczur może wchodzić do wody.
# • Normalnym ruchem jest przesunięcie bierki na sąsiednie wolne pole, w kierunku góra, dół,
# lewo, lub prawo.
# • Tygrys i lew mogą skakać przez stawy (aby wykonać skok, bierka musi „tak jakby” wejść na staw
# i następnie poruszać się w tym samym kierunku aż do osiągnięcia pola niebędącego stawem).
# Nie wolno skakać nad wrogim szczurem.
# • Wejście na pole zajęte przez inną bierkę jest równoważne z jej zbiciem. Można bić bierkę o
# równej sile albo słabszą. Szczur (wbrew starszeństwu) jest silniejszy od słonia. Poza tym
# starszeństwo bierek odpowiada ich sile.
# • Szczur nie może bić, wykonując ruch z jeziora do lądu.
# • Bierka znajdująca się w pułapce (jednym z pól otaczających jamę), traci całkowicie swoją siłę
# i może być zbita przez dowolną bierkę.
# • Celem gry jest wejście bierką do jamy przeciwnika. Po takim ruchu gra się kończy i wygrywa
# gracz wchodzący do jamy.
# Te tradycyjne zasady wymagają drobnego skomplikowania, żeby utrudnić trywialną grę na remis
# przez obudowywanie swojej jamy zasiekami „nie do przejścia”. Nowa reguła brzmi następująco:
# Jeżeli przez kolejne 30 ruchów nie nastąpi bicie (albo wejście do jamy), wówczas gra się
# kończy i zwycięstwo ustala się:
# • porównując starszeństwo bierek: wygrywa gracz, który ma najstarszą bierkę, nie-
# posiadaną przez drugiego gracza,
# • a jeżeli gracze mają dokładnie te same bierki, wówczas wygrywa gracz, który po-
# ruszał się jako drugi.






