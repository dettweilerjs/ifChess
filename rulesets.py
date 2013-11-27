import g

fileRead = g.fileRead

###################### THIS IS THE REGULAR CHESS RULESET ##################################

class reg:

	def move(self, orig, dest, attack): # moves a piece if it is legal to move it

		player = g.player		
		r = int(dest[0])
		f = int(dest[2])
		c = str(player)
		d = abs(player - 1) * 2 - 1 # gives the direction player is moving (+1 or -1): see threatens: pawn for more info
		piece = orig[0]
		
		coords = reg.findPiece(self, piece, orig, r, f) # locate piece, since algebraic notation doesn't always specify exact location

		if not coords: # findPiece returns false if there are no possible pieces
			return "Illegal move"
		else:
			orig = coords[-1]
			coords = coords[:-1] # strip orig from coords[]
			if len(coords) > 2: # i.e. there is more than one piece threatening chessBoard[r][f]
				return "Please specify which piece to use"
		
		if piece == "o": piece = ""
		if attack and g.chessBoard[r][f] == " " and not g.passant: # trying to attack an empty square
			return "Not a capture. Use " + piece + orig + str(fileRead[f]) + str(r + 1) + " instead."
		elif not attack and not g.chessBoard[r][f] == " ": # trying to move to an occupied square
			return "Not a move. Use " + piece + orig + "x" + str(fileRead[f]) + str(r + 1) + " instead."

		temp = g.chessBoard[r][f]
		g.chessBoard[r][f] = g.chessBoard[coords[0]][coords[1]]
		g.chessBoard[coords[0]][coords[1]] = " "
		if g.passant: g.chessBoard[r - d][f] = " "
		if reg.check(self):
			g.chessBoard[coords[0]][coords[1]] = g.chessBoard[r][f]
			g.chessBoard[r][f] = temp
			if g.passant: g.chessBoard[r - d][f] = str(abs(player - 1)) + "o"
			return "Must avoid check"
		if attack:
			if g.passant: g.lost.append(str(abs(player - 1)) + "o")
			else: g.lost.append(temp[:2])
		if (piece == "K" or piece == "R") and (not g.chessBoard[r][f][-1] == "m"):
			g.chessBoard[r][f] = g.chessBoard[r][f] + "m"
		return 0


	def castle(self, q):
		
		player = g.player
		c = str(player)
		n = player * 7 # if player is 0 (white), castles happen on rank 0; if player is 1 (black), castles happen on rank 7
		
		if q == "q": # queenside castling
			if (not g.chessBoard[n][2] == " " or not g.chessBoard[n][3] == " "
			or reg.threatened(self, n, 2) or  reg.threatened(self, n, 3)
			or reg.check(self) or not g.chessBoard[n][0] == c + "R"
			or not g.chessBoard[n][4] == c + "K"):
				return "Illegal castle"
			g.chessBoard[n][4] = " "
			g.chessBoard[n][2] = c + "Km"
			g.chessBoard[n][0] = " "
			g.chessBoard[n][3] = c + "Rm"
			return 0
		else: # kingside
			if (not g.chessBoard[n][5] == " " or not g.chessBoard[n][6] == " "
			or reg.threatened(self, n, 5) or  reg.threatened(self, n, 6)
			or reg.check(self) or not g.chessBoard[n][7] == c + "R"
			or not g.chessBoard[n][4] == c + "K"):
				return "Illegal castle"
			g.chessBoard[n][4] = " "
			g.chessBoard[n][6] = c + "Km"
			g.chessBoard[n][7] = " "
			g.chessBoard[n][5] = c + "Rm"
			return 0


	def queened(): # if queened, returns a character containing what the queened pawn was updated to; else, returns False

		player = g.player		
		c = str(player)
		n = abs(player - 1) * 7 # same as castle; but queening happens on the other end of the board

		for i in range(8):
			if g.chessBoard[n][i] == c + "o":
				role = str.lower(input("--> Become (Q,R,B,N): "))
				while True:
					if role == "q":
						g.chessBoard[n][i] = c + "Q"
						return "Q"
					elif role == "r":
						g.chessBoard[n][i] = c + "Rm"
						return "R"
					elif role == "b":
						g.chessBoard[n][i] = c + "B"
						return "B"
					elif role == "N":
						g.chessBoard[n][i] = c + "N"
						return "N"
					else:
						print("Unknown input")
						role = str.lower(input("--> Become (Q,R,B,N): "))
		return False
	

	def check(self): # Returns True if player is in check; else, returns False
	
		player = g.player
		c = str(player)

		for i in range(8):
			for j in range(8):
				if g.chessBoard[i][j][:2] == c + "K" and reg.threatened(self, i, j): # if the king is threatened
					return True
		return False


	def mate(self): # Returns true if player is mated; else returns false

		player = g.player
		d = abs(player - 1) * 2 - 1

		if reg.check(self):
		
			coords = []
			c = str(player)

			for i in range(8):
				for j in range(8):
					if g.chessBoard[i][j][0] == c: # find all pieces of the same color and list their coordinates
						coords.append(i)
						coords.append(j)
			for i in range(8):
				for j in range(8):
					for k in range(0,len(coords) - 1,2): # for each piece in coords[]...
						if self.threatens(coords[k], coords[k + 1], i, j): # if it can move/capture somewhere...
							temp = g.chessBoard[i][j]
							g.chessBoard[i][j] = g.chessBoard[coords[k]][coords[k + 1]]
							g.chessBoard[coords[k]][coords[k + 1]] = " " # do it...
							if g.passant: g.chessBoard[i - d][j] = " "
							if not reg.check(self): # if not in check anymore...
								g.chessBoard[coords[k]][coords[k + 1]] = g.chessBoard[i][j]
								g.chessBoard[i][j] = temp # undo it and return false
								if g.passant: g.chessBoard[r - d][f] = str(abs(player - 1)) + "o"
								return False
							g.chessBoard[coords[k]][coords[k + 1]] = g.chessBoard[i][j]
							g.chessBoard[i][j] = temp # otherwise, just undo it
							if g.passant: g.chessBoard[r - d][f] = str(abs(player - 1)) + "o"
			return True
			
		return False

	
	def victory(self): # 

		c = str(abs(g.player - 1))

		if reg.mate(self):
			return "#"
		elif g.isChess2:
			for i in range(8):
				if g.chessBoard[4 - abs(g.player - 1)][i][:2] == c + "K": # if a King has crossed the midline
					return "^"
		return False


	def findPiece(self, piece, orig, r, f): # Returns coords of all possible "piece" on board; else, returns False
							# so zen
		player = g.player
		startr = -1
		startf = -1
		coords = [-1,-1]
		c = str(player)
		if len(orig) == 4: # if rank and file are both specified
			startr = int(orig[-2]) - 1
			startf = int(orig[-1])
			orig = orig[1:3] # for wrong notation notification
		elif len(orig) == 3: # if file is specified
			startf = int(orig[-1])
			orig = orig[1]
		elif len(orig) == 2: # if rank is specified
			startr = int(orig[-1]) - 1
			orig = orig[1]
		else:
			orig = ""

		for i in range(8):
			for j in range(8):
				if len(g.chessBoard[i][j]) > 1 and g.chessBoard[i][j][:2] == c + piece:
					coords.append(i)
					coords.append(j)

		for k in range(0, len(coords) - 1,2):
			if ((startr > -1 and not coords[k] == startr) # piece must be on specified rank or file, if there is one
			or (startf > -1 and not coords[k + 1] == startf)
			or (not self.threatens(coords[k], coords[k + 1], r, f))): # piece must be attacking given square
				coords[k] = -1
				coords[k + 1] = -1

		coords = [x for x in coords if not x == -1]

		if len(coords) > 0:
			coords.append(orig)
			return coords

		return False

	
	def threatened(self, r, f): # global threat check for a given square

		g.player = abs(g.player - 1)
		for i in range(8):
			for j in range(8):
				if self.threatens(i, j, r, f): # calls threatens with the opposite player for all squares on board
					g.player = abs(g.player - 1)
					return True
		g.player = abs(g.player - 1)
		return False


	def threatens(startr, startf, r, f): # returns True if piece on startr, startf threatens r, f; else, returns False

		player = g.player
		c = str(player)

		if startr == r and startf == f: # if called referencing the same start and finish square
			return False
		if g.chessBoard[startr][startf][0] == g.chessBoard[r][f][0]: # if the two squares contain the same color pieces
			return False
		if g.chessBoard[startr][startf] == " ": # if the start square is empty
			return False
		if (g.rules[abs(player - 1)] == nem and g.chessBoard[r][f] == str(abs(player - 1)) + "Q" 
			and not g.chessBoard[startr][startf][:2] == c + "K"): # if the piece under attack is a Nemesis and the attacker is not a King
			return False
		if g.rules[abs(player - 1)] == rpr and g.chessBoard[r][f][:2] == str(abs(player - 1)) + "R": # if piece under attack is Reaper rook
			return False

		if g.chessBoard[startr][startf][:2] == c + "K": # if King
			
			if r - startr in range(-1, 2) and f - startf in range(-1, 2):
				return True

			return False		

		elif g.chessBoard[startr][startf] == c + "Q": # if Queen

			if (r == startr): # squares are on the same rank and no pieces in between
				n = f - startf
				for i in range((n//abs(n)), n,(n//abs(n))): # counts up from one or down from negative one
					if not g.chessBoard[r][startf + i] == " ":
						return False
				return True
			elif (f == startf): # squares are on the same file and no pieces in between
				n = r - startr
				for i in range((n//abs(n)), n,(n//abs(n))):
					if not g.chessBoard[startr + i][f] == " ":
						return False
				return True
			elif abs(r - startr) == abs(f - startf): # squares are in a diagonal line
				k = r - startr
				l = abs(k)
				n = f - startf
				p = abs(n)
				for i in range(1,l):
					if not g.chessBoard[startr + (k//l) * i][startf + (n//p) * i] == " ":
						return False
				return True
			
			return False

		elif g.chessBoard[startr][startf][:2] == c + "R": # if Rook

			if (r == startr): # squares are on the same rank and no pieces in between
				n = f - startf
				for i in range((n//abs(n)), n,(n//abs(n))): # counts up from one or down from negative one
					if not g.chessBoard[r][startf + i] == " ":
						return False
				return True
			elif (f == startf): # squares are on the same file and no pieces in between
				n = r - startr
				for i in range((n//abs(n)), n,(n//abs(n))):
					if not g.chessBoard[startr + i][f] == " ":
						return False
				return True

			return False

		elif g.chessBoard[startr][startf] == c + "N": # if Knight

			k = abs(r - startr)
			l = abs(f - startf)

			if (not k == l) and k in [2,1] and l in [2,1]:
				return True

			return False

		elif g.chessBoard[startr][startf] == c + "B": # if Bishop

			k = r - startr
			l = abs(k)
			n = f - startf
			p = abs(n)
			
			if l == p:
				for i in range(1,l):
					if not g.chessBoard[startr + (k//l) * i][startf + (n//p) * i] == " ":
						return False
				return True

			return False

		elif g.chessBoard[startr][startf] == c + "o": # if pawn

			d = abs(player - 1) * 2 - 1 # gives the direction pawns are going 0 (white) transforms to 1 * 2 - 1
							# = 1 = moving up the board; 1 (black) transforms to 0 * 2 - 1 = -1 = moving down the board
			n = player * 7

			if not g.chessBoard[r][f] == " ":
				if r == startr + d and (f == startf - 1 or f == startf + 1): # diagonal capture
					return True
			elif g.chessBoard[r][f] == " ":
				if r == startr + d and f == startf: # pawn move
					return True
				elif (g.chessBoard[r][f] == " " and startr == n + d and r == n + 3 * d # double move from home rank
					and f == startf and g.chessBoard[n + 2 * d][f] == " "):
					return True
				elif (g.turn > 1 and r == startr + d and (f == startf - 1 or f == startf + 1)
					and fileRead[f] == g.moveList[-1][0] and r - d == int(g.moveList[-1][1]) - 1): # en passant
					g.passant = True
					return True

			return False
		
		return False

###################### END OF REGULAR CHESS RULESET ##################################


####################### THIS IS THE NEMESIS RULESET ##################################

class nem:

	def move(self, orig, dest, attack):
		
		return reg.move(self, orig, dest, attack)


	def castle(self, q):

		return "Only Classic Army can castle."

	
	def victory(self):
	
		return reg.victory(self)


	def threatens(startr, startf, r, f):
		
		player = g.player
		c = str(player)

		if startr == r and startf == f:
			return False

		if g.chessBoard[startr][startf] == c + "Q": # if Queen

			if not (g.chessBoard[r][f] == " " or g.chessBoard[r][f][:2] == str(abs(player - 1)) + "K"):
				return False
		
		elif g.chessBoard[startr][startf] == c + "o": # if pawn

			d = abs(player - 1) * 2 - 1
			n = player * 7
			coords = []
			for i in range(8):
				for j in range(8):
					if g.chessBoard[i][j][:2] == str(abs(player - 1)) + "K":
						coords.append(i)
						coords.append(j)
						
			if g.chessBoard[r][f] == " ":
				for i in range(0,len(coords) - 1,2):
					if (coords[i] == startr and abs(coords[i + 1] - startf) > 1 and r == startr
						and abs(startf - coords[i + 1]) - abs(f - coords[i + 1]) == 1):
						return True
					elif (coords[i + 1] == startf and abs(coords[i] - startr) > 1 and f == startf
						and abs(startr - coords[i]) - abs(r - coords[i]) == 1):
						return True
					elif not (coords[i + 1] == startf or coords[i] == startr):
						a = (coords[i] - startr)//abs(coords[i] - startr)
						b = (coords[i + 1] - startf)//abs(coords[i + 1] - startf)
						if ((r in range(startr, coords[i] + a, a)
							and f in range(startf, coords[i + 1] + b, b)
							and abs(startr - r) < 2 and abs(startf - f) < 2)):
							return True
				if (startr == n + d and r == n + 3 * d and f == startf):
					return False
		
		return reg.threatens(startr, startf, r, f)

############################ END OF NEMESIS RULESET ##################################


####################### THIS IS THE EMPOWERED RULESET ################################

class emp:

	def move(self, orig, dest, attack):
		
		return reg.move(self, orig, dest, attack)


	def castle(self, q):

		return "Only Classic Army can castle."

	
	def victory(self):
	
		return reg.victory(self)


	def threatens(startr, startf, r, f):
		
		player = g.player
		c = str(player)

		if startr == r and startf == f:
			return False

		if g.chessBoard[startr][startf] == c + "Q": # if Queen

			if not (r - startr in range(-1, 2) and f - startf in range(-1, 2)):
				return False
		
		elif (g.chessBoard[startr][startf][:2] == c + "R" or g.chessBoard[startr][startf] == c + "N"
			or g.chessBoard[startr][startf] == c + "B"): # if Rook, Bishop, or Knight

			temp = g.chessBoard[startr][startf]
			for i in [-1,1]:
				if startr + i in range(8):
					if g.chessBoard[startr + i][startf] == c + "B":
						g.chessBoard[startr][startf] = c + "B"
					elif g.chessBoard[startr + i][startf] == c + "N":
						g.chessBoard[startr][startf] = c + "N"
					elif g.chessBoard[startr + i][startf][:2] == c + "R":
						g.chessBoard[startr][startf] = c + "R"
					
					if reg.threatens(startr, startf, r, f):
						g.chessBoard[startr][startf] = temp
						return True
					g.chessBoard[startr][startf] = temp

				if startf + i in range(8):
					if g.chessBoard[startr][startf + i] == c + "B":
						g.chessBoard[startr][startf] = c + "B"
					elif g.chessBoard[startr][startf + i] == c + "N":
						g.chessBoard[startr][startf] = c + "N"
					elif g.chessBoard[startr][startf + i][:2] == c + "R":
						g.chessBoard[startr][startf] = c + "R"
					
					if reg.threatens(startr, startf, r, f):
						g.chessBoard[startr][startf] = temp
						return True
					g.chessBoard[startr][startf] = temp
		
		return reg.threatens(startr, startf, r, f)

############################ END OF EMPOWERED RULESET ################################


########################## THIS IS THE REAPER RULESET ################################

class rpr:

	def move(self, orig, dest, attack):
		
		return reg.move(self, orig, dest, attack)


	def castle(self, q):

		return "Only Classic Army can castle."

	
	def victory(self):
	
		return reg.victory(self)


	def threatens(startr, startf, r, f):
		
		player = g.player
		c = str(player)

		if startr == r and startf == f:
			return False

		if g.chessBoard[startr][startf] == c + "Q": # if Queen

				# Queen can capture anywhere but back row, anyone but King
			if (not r == 7 - (7 * player) and not g.chessBoard[r][f][:2] == str(abs(player - 1)) + "K"):
				return True
			return False
		
		elif g.chessBoard[startr][startf][:2] == c + "R": # if Rook

			if g.chessBoard[r][f] == " ": # Rooks can't capture or be captured, but can move to any open spot
				return True
			return False
		
		return reg.threatens(startr, startf, r, f)

############################### END OF REAPER RULESET ################################

