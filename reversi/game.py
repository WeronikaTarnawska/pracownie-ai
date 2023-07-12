import copy


class Game:
	def __init__(self, ini):
		self.n = 8
		self.history = []
		self.fliplist = []
		self.cur_player = 0
		self.free = set()
		self.board = []
		if ini:
			self.board = [['.' for _ in range(self.n)] for _ in range(self.n)]
			self.board[3][4], self.board[4][3], self.board[3][3], self.board[4][4] = 0, 0, 1, 1
			for i in range(self.n):
				for j in range(self.n):
					if (i, j) not in ((3, 4), (4, 3), (3, 3), (4, 4)):
						self.free.add((i, j))

	def moves_gen(self):
		me, him = self.cur_player, 1 - self.cur_player
		moves = []
		for (px, py) in self.free:
			for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
				x, y, i = px + dx, py + dy, 0
				while 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == him:
					x += dx
					y += dy
					i += 1
				if 0 <= x < self.n and 0 <= y < self.n and i > 0 and self.board[x][y] == me:
					moves.append((px, py))
					break
		return moves

	def make_move(self, move):
		me, him = self.cur_player, 1 - self.cur_player
		self.history.append((me, move))
		self.cur_player = 1 - self.cur_player
		if not move:
			self.fliplist.append([])
			return
		xm, ym = move
		self.board[xm][ym] = me
		self.free.remove(move)
		fl = []
		for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
			x, y = xm + dx, ym + dy
			to_flip = []
			while 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == him:
				to_flip.append((x, y))
				x += dx
				y += dy
			if 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == me:
				for (a, b) in to_flip:
					self.board[a][b] = me
				fl += to_flip
		self.fliplist.append(fl)

	def undo_move(self):
		if not self.history:
			return
		me, move = self.history[-1]
		him = 1-me
		to_flip = self.fliplist[-1]
		self.fliplist = self.fliplist[:-1]
		self.history = self.history[:-1]
		self.cur_player = 1 - self.cur_player
		if not move:
			return
		xm, ym = move
		self.board[xm][ym] = '.'
		self.free.add(move)
		for (a, b) in to_flip:
			self.board[a][b] = him

	def print_board(self):
		print(f'player {self.cur_player} moves')
		for line in self.board:
			for x in line:
				print(x, end="")
			print()

	def endgame(self):
		if len(self.history) < 2:
			return False
		if not self.free:
			return True
		if not self.history[-1][1] and not self.history[-2][1]:
			return True
		return False

	def board_count(self, a, b):
		ac, bc = 0, 0
		for line in self.board:
			for i in line:
				if i == a:
					ac += 1
				elif i == b:
					bc += 1
		return ac, bc

	def copy_game(self):
		g = Game(False)
		g.board = [[self.board[i][j] for j in range(len(self.board[0]))] for i in range((len(self.board)))]
		g.history = [i for i in self.history]
		g.cur_player = self.cur_player
		g.free = copy.deepcopy(self.free)
		g.fliplist = [[(self.fliplist[a][b][c] for c in range(2)) for b in range(len(self.fliplist[a]))] for a in range(len(self.fliplist))]
		return g


