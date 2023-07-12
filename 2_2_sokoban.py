import copy
import queue
import time

class Board:
    def __init__(self, m, bb, skrzynki, h):
        self.ludek = m
        self.box = bb
        self.bs = skrzynki
        # self.possibles = sa  # skrzynki w tej składowej + możliwości popchnięcia
        self.history = h
        self.pri = len(h)

    def __lt__(self, other):
        return self.pri < other.pri

    def __le__(self, other):
        return self.pri <= other.pri

    def __gt__(self, other):
        return self.pri > other.pri

    def __ge__(self, other):
        return self.pri >= other.pri

    def __eq__(self, other):
        return self.pri <= other.pri


def read_input():
    global b0, wall, goal, height, width
    fin = open("zad_input.txt", 'r')
    wall = []
    goal = []
    box = []
    skrzynki = set()
    row = 0
    mag = []
    while line := fin.readline()[:-1]:
        w = [False for i in range(len(line))]
        g = [False for i in range(len(line))]
        b = [False for i in range(len(line))]
        for x in range(len(line)):
            if line[x] == "W":
                w[x] = True
            elif line[x] == "G":
                g[x] = True
            elif line[x] == "B":
                skrzynki.add((row, x))
                b[x] = True
            elif line[x] == "K":
                mag.append((row, x))
            elif line[x] == "*":
                skrzynki.add((row, x))
                b[x] = True
                g[x] = True
            elif line[x] == "+":
                mag.append((row, x))
                g[x] = True
        wall.append(w)
        goal.append(g)
        box.append(b)
        row += 1
    fin.close()
    height = len(wall)
    width = len(wall[0])
    return Board(mag[0], box, skrzynki, ""), wall, goal, height, width


def printboard(b):
    # print("\n".join([str(row) for row in tab]))
    for i in range(height):
        for j in range(width):
            if wall[i][j]:
                print("#", end="")
            elif b.box[i][j]:
                print("B", end="")
            elif b.ludek[0] == i and b.ludek[1] == j:
                print("0", end="")
            elif goal[i][j]:
                print("*", end="")
            else:
                print(" ", end="")
        print()
    print()


def write_out(lab):
    fout = open("zad_output.txt", 'w')
    fout.write(lab.history + '\n')
    # printss(lab)
    fout.close()
    # exit()


def up(b):
    m = b.ludek
    moved = False
    if not wall[m[0] - 1][m[1]]:
        if b.box[m[0] - 1][m[1]]:
            if not wall[m[0] - 2][m[1]] and not b.box[m[0] - 2][m[1]]:
                b.box[m[0] - 1][m[1]] = False
                b.box[m[0] - 2][m[1]] = True
                b.bs.remove((m[0] - 1, m[1]))
                b.bs.add((m[0]-2, m[1]))
                b.ludek = (m[0] - 1, m[1])
                moved = True
        else:
            b.ludek = (m[0] - 1, m[1])
            moved = True
    if moved:
        b.history += "U"
    return moved


def down(b):
    m = b.ludek
    moved = False
    if not wall[m[0] + 1][m[1]]:
        if b.box[m[0] + 1][m[1]]:
            if not wall[m[0] + 2][m[1]] and not b.box[m[0] + 2][m[1]]:
                b.box[m[0] + 1][m[1]] = False
                b.box[m[0] + 2][m[1]] = True
                b.bs.remove((m[0] + 1, m[1]))
                b.bs.add((m[0] + 2, m[1]))
                b.ludek = (m[0] + 1, m[1])
                moved = True
        else:
            b.ludek = (m[0] + 1, m[1])
            moved = True
    if moved:
        b.history += "D"
    return moved


def left(b):
    m = b.ludek
    moved = False
    if not wall[m[0]][m[1]-1]:
        if b.box[m[0]][m[1]-1]:
            if not wall[m[0]][m[1]-2] and not b.box[m[0]][m[1]-2]:
                b.box[m[0]][m[1]-1] = False
                b.box[m[0]][m[1]-2] = True
                b.bs.remove((m[0], m[1]-1))
                b.bs.add((m[0], m[1]-2))
                b.ludek = (m[0], m[1]-1)
                moved = True
        else:
            b.ludek = (m[0], m[1]-1)
            moved = True
    if moved:
        b.history += "L"
    return moved


def right(b):
    m = b.ludek
    moved = False
    if not wall[m[0]][m[1]+1]:
        if b.box[m[0]][m[1]+1]:
            if not wall[m[0]][m[1]+2] and not b.box[m[0]][m[1]+2]:
                b.box[m[0]][m[1]+1] = False
                b.box[m[0]][m[1]+2] = True
                b.bs.remove((m[0], m[1] + 1))
                b.bs.add((m[0], m[1] + 2))
                b.ludek = (m[0], m[1]+1)
                moved = True
        else:
            b.ludek = (m[0], m[1] + 1)
            moved = True
    if moved:
        b.history += "R"
    return moved


def check(b):
    for x in b.bs:
        if not goal[x[0]][x[1]]:
            return False
    return True


def b2str(b):
    t = list(b.bs)
    t.sort()
    t.append(b.ludek)
    return tuple(t)


def putq(fun, b, que, done):
    bb = copy.deepcopy(b)
    if fun(bb):
        s = b2str(bb)
        if s not in done:
            done.add(s)
            que.put(bb)


def bfs(bstart):
    que = queue.Queue()
    que.put(bstart)
    done = set()
    done.add(b2str(bstart))
    while not que.empty():
        b = que.get()
        # print(b.history)
        if check(b):
            write_out(b)
            return True
        putq(left, b, que, done)
        putq(right, b, que, done)
        putq(up, b, que, done)
        putq(down, b, que, done)
    return False


b0, wall, goal, height, width = read_input()
# printboard(b0)
# print(b2str(b0))
t1 = time.perf_counter()
bfs(b0)
t2 = time.perf_counter()
print(t2 - t1)

# [[False for i in range(0,len(file[0]))] for i in range(0,len(file))]
