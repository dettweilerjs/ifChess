import platform

chessBoard = [[] for x in range(8)] 		# creates an 8x8 chessboard matrix
isChess2 = False				# differentiates between chess and chess 2
rules = [] 					# chess2 implementation for different rulesets
fileRead = ["a","b","c","d","e","f","g","h"]	# index of letter is file index of that letter on the chess board
pieces = ["K","Q","R","N","B","o"]		# list of piece markers - used for checking valid pieces
moveList = []					# stores moves played 
lost = []					# retains pieces lost by both sides, in order of time lost
turn = 1					# increases by one each round
player = 0					# changes between 0 and 1 based on whose turn it is
passant = False					# en passant boolean

if platform == "win32":
	CLS_CMD = "cls"
else:
	CLS_CMD = "clear"
