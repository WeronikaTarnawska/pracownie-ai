import random


def pick_move(s, me):
    possibles = s.moves_gen()
    if possibles:
        return random.choice(possibles)
    else:
        return ()
