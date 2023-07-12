# python3 validator.py zad5 python3 storms_for_students.py

def v(x, y):
    return 'B_%d_%d' % (x, y)


def domains(vs):  # Zmienne, dziedziny: piksele, 0..1
    return [q + ' in 0..1' for q in vs]


def v_sum(row, suma, width):
    s = v(row, 0)
    for i in range(1, width):
        s += " + " + v(row, i)
    s += " #= " + str(suma)
    return s


def h_sum(col, suma, height):
    s = v(0, col)
    for i in range(1, height):
        s += " + " + v(i, col)
    s += " #= " + str(suma)
    return s


def sums(width, height, rsum, csum):  # Radary: b1 + b2 + · · · + bn = K
    s = [v_sum(r, rsum[r], width) for r in range(height)] + [h_sum(c, csum[c], height) for c in range(width)]
    return s


def ok3(a, b, c):  # warunek na prostokąt 3*1 lub 1*3
    return f'{a} + 2 * {b} + 3 * {c} #\= 2'


def rectangles(width, height):
    s = [ok3(v(i, j), v(i, j+1), v(i, j+2)) for i in range(height) for j in range(width-2)]\
        + [ok3(v(i, j), v(i+1, j), v(i+2, j)) for j in range(width) for i in range(height-2)]
    return s


def ok22(aa, ab, ba, bb):  # warunek na kwadrat 2*2
    # s = f'{aa} + {ab} + {ba} + {bb} #\= 3'
    # f'{aa} + {ab} + {ba} + {bb} = 2 -> {aa} != {bb}'
    # f'(({aa} <=> {ab}) & ({ba} <=> {bb})) | (({aa} <=> {ba}) & ({ab} <=> {bb}))'
    s = f'tuples_in([[{aa}, {ab}, {ba}, {bb}]], [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], ' \
        '[0, 0, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1]])'
    return s


def squares(width, height):
    return [ok22(v(i, j), v(i, j+1), v(i+1, j), v(i+1, j+1)) for i in range(height-1) for j in range(width-1)]


def all_different(qs):
    return 'all_distinct([' + ', '.join(qs) + '])'


def ctriples(tripl):
    return [f'{v(t[0], t[1])} #= {t[2]}' for t in tripl]


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    height = len(rows)
    width = len(cols)

    variables = [v(i, j) for i in range(height) for j in range(width)]

    writeln('solve([' + ', '.join(variables) + ']) :- ')

    constraints = domains(variables) + sums(width, height, rows, cols) + rectangles(width, height) \
                  + squares(width, height) + ctriples(triples)

    for x in constraints:
        writeln(x + ",")

    writeln('    labeling([ff], [' + ', '.join(variables) + ']).')
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for ii in range(2, len(txt)):
    if txt[ii].strip():
        triples.append(list(map(int, txt[ii].split())))

storms(rows, cols, triples)
