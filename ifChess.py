from rulesets import * # currently imports reg(regular chess) and nem(nemesis)
import g
import os

armies = [reg,nem,emp,rpr]
g.rules = [reg,reg]
CLS_CMD = g.CLS_CMD
fileRead = g.fileRead
pieces = g.pieces

class ifChess:

	def main():

		os.system(CLS_CMD)
		print("Welcome to IfChess! ©Joel Dettweiler")
		print("What would you like to play?")
		opt = input("--> [C]hess or Chess [2]: ")
		if str.lower(opt) in ["chess 2","chess2","2"]:
			ifChess.setRules()
			g.isChess2 = True
		opt = input("--> Configure? (y/n): ")
		if str.lower(opt) in ["y","yes","ye"]: ifChess.layout()
		else: ifChess.setup()
		os.system(CLS_CMD)
		ifChess.printBoard()
		print("Welcome to Chess 2! Type moves in algebraic notation.")
		print("	Type [H]elp for command list.")
		opt = input("--> ")
		while True:
			ifChess.execute(opt)
			os.system(CLS_CMD)
			ifChess.printBoard()
			opt = input("--> ")


	def printBoard(board = g.chessBoard):	# given a chessboard matrix, print it

		for i in range(7,-1,-1):		# in order to print from top to bottom
			print(str(i + 1),end=" ")	# prints rank labels to the left of the board
			for j in range(8):
				if board[i][j][0] == "1":	# if square contains a black piece
					print("[" + "\033[1m" + board[i][j][1] + "\033[0m" + "]", end="") # print it bold
				elif board[i][j][0] == "0":
					print("[" + board[i][j][1] + "]", end="")	# print a white piece
				else:
					print("[" + board[i][j] + "]", end="")		# print a blank square
			print("")
		print("  ",end="") # these three lines print the file labels below the board
		for k in range(8):
			print(" " + fileRead[k] + " ",end="")
		print()
		print()


	def printMoveList(): # prints all moves made up to this point

		moveList = g.moveList
		
		for i in range(0, len(moveList), 2):
			print(str((i // 2) + 1).rjust(2),end=" ") # label turn numbers
			print(moveList[i].ljust(9),end="")
			if i + 1 < len(moveList):
				print(moveList[i + 1].ljust(7),end="")
			print()

	
	def printLost(): # prints all captured pieces

		wtemp = []
		btemp = []
		i = input("--> By [r]ank or in [o]rder: ")
		if i in ["rank","r"]:
			for j in range(1,6):
				for k in g.lost:
					if k == ("0" + pieces[j]):
						wtemp.append(k)
					elif k == ("1" + pieces[j]):
						btemp.append(k)
		else:
			for k in g.lost:
				if k[0] == "0":
					wtemp.append(k)
				elif k[0] == "1":
					btemp.append(k)

		print("	White: ", end = "")
		print("\033[1m",end = "")
		for n in btemp:
			print(n[1], end = " ")
		print()
		print("	Black" + "\033[0m" + ": ", end = "")
		for l in wtemp:
			print(l[1], end = " ")
		print()
		

	def printHelp(): # prints a list of available commands

		print("[Q]uit or [E]xit: End program")
		print("[R]ecord: View previous moves")
		print("[T]urn: Check whose turn it is")
		print("[P]ieces: Show captured pieces")
		print("[M]ove: Display move commands")
		print("[A]rmies: See opposing armies")


	def layout():

		for i in range(8):
			for j in range(8):
				g.chessBoard[i].append(" ")
		os.system(CLS_CMD)
		ifChess.printBoard()
		print("Input pieces in this format - piece:square.")
		print("Use a blank space before : to overwrite square.")
		print("Input white pieces. Type [D]one when all have been placed")
		place = input("--> ")
		c = 0
		while True:

			if c == 0 and str.lower(place) in ["done","d",""]:
				c = 1
				print("Input black pieces. Type [D]one when all have been placed")
				place = input("--> ")
			elif c == 1 and str.lower(place) in ["done","d",""]:
				break
			elif (not len(place) == 4 or (place[0] not in pieces 
				and not place[0] == " ") or not place[1] == ":"
				or place[2] not in fileRead or int(place[3]) not in range(1,9)):
				print("Unknown input")
				place = input("--> ")
			else:
				place = place.split(":")
				place[1] = ifChess.convertSquare(place[1]).split(" ")
				g.chessBoard[int(place[1][0])][int(place[1][1])] = str(c) + place[0]
				os.system(CLS_CMD)
				ifChess.printBoard()
				place = input("--> ")


	def setup():	# sets the chessboard matrix to a default chess setup

		# "1" before a piece denotes that it is a black piece, "0" for white

		g.chessBoard[7] = ["1R","1N","1B","1Q","1K","1B","1N","1R"]	# setting up back rows on both sides
		g.chessBoard[0] = ["0R","0N","0B","0Q","0K","0B","0N","0R"]
		for i in range(8):
			g.chessBoard[6].append("1o")	# black pawns
			for j in range(2,6):
				g.chessBoard[j].append(" ")	# empty squares
			g.chessBoard[1].append("0o")	# white pawns


	def setRules():
		
		print("1: Classic")
		print("2: Nemesis")
		print("3: Empowered")
		print("4: Reaper")
		print("5: Warrior Kings")
		print("6: Animals")
		k = "7"
		j = "7"
		while int(k) - 1 not in range(6):
			k = input("--> White (1-6): ")
		while int(j) - 1 not in range(6):
			j = input("--> Black (1-6): ")
		g.rules[0] = armies[int(k) - 1]
		g.rules[1] = armies[int(j) - 1]
		


	def execute(strat): # processes input and sends it to proper destination
		
		bad = "Unknown input"	# ruleset changes "bad" to 0 if it is a legal move
	
		if str.lower(strat) in ["help","h"]:
			ifChess.printHelp()
			ifChess.execute(input("--> "))
			return
		elif strat == "" or str.lower(strat) in ["quit","q","exit","e"]:
			i = input("--> Exit? (y/n): ")
			if str.lower(i) in ["yes","y"]:
				exit()
			ifChess.execute(input("--> "))
			return
		elif str.lower(strat) in ["record","r"]:
			ifChess.printMoveList()
			ifChess.execute(input("--> "))
			return
		elif str.lower(strat) in ["turn","t"]:
			if g.player:
				print("It is Black's turn.")
			else:
				print("It is White's turn.")
			ifChess.execute(input("--> "))
			return
		elif str.lower(strat) in ["pieces","p"]:
			ifChess.printLost()
			ifChess.execute(input("--> "))
			return
			

		########################### ALGEBRAIC NOTATION TRANSLATOR ################################

		if (strat == "O-O-O") or (strat == "0-0-0"): # castling
			bad = g.rules[g.player].castle(g.rules[g.player], "q")
		elif (strat == "O-O") or (strat == "0-0"): # castling kingside
			bad = g.rules[g.player].castle(g.rules[g.player], "k")
		elif len(strat) > 1:

			attack = False
			info = [strat[:-2],strat[-2:]]

			if info[0] == "" or info[0] in fileRead: # pawn move
				info[0] = "o" + info[0]
			if info[0][-1] == "x": # if move is an attack
				attack = True
				info[0] = info[0][:-1] # remove "x" from info[0]
			if info[0][0] in fileRead and attack: # pawn attack (i.e. axb6)
				info[0] = "o" + info[0] # add pawn marker
			if len(info[0]) > 1 and info[0][1] in fileRead: # if notation specifies a file
				info[0] = info[0] + str(fileRead.index(info[0][1])) # append numeric interpretation of file*
			if (((info[0][-1] in pieces) or (info[0][-1] in [str(k) for k in range(8)]) or (info[0][-1] in fileRead))
				and (len(info[1]) == 2) and (info[1][0] in fileRead) and (int(info[1][1]) in range(1,9))): # if this is algebraic notation				
				bad = g.rules[g.player].move(g.rules[g.player], info[0], ifChess.convertSquare(info[1]), attack)

		# *Qbxd3 is represented info[Qb1,d3], Q1xd3 == info[Q1,d3], Qb1xd3 == info[Qb11,d3]
		###########################################################################################

		if bad:
			print(bad)
			ifChess.execute(input("--> "))
		else:
			win = False

			q = reg.queened()		
			if q:
				strat = strat + "=" + q
			if g.passant: # if move was en passant
				strat = strat + "e.p."
				g.passant = False # reset
			g.player = abs(g.player - 1) # change player
			v = g.rules[g.player].victory(g.rules[g.player])
			if v:
				strat = strat + v
				win = True
			elif reg.check(g.rules[g.player]): strat = strat + "+"

			g.moveList.append(strat)
			if not g.player: # if it is now White's turn
				g.turn = g.turn + 1

			if win:
				os.system(CLS_CMD)
				ifChess.printBoard()
				ifChess.printMoveList()
				input()
				exit()


	def convertSquare(square):	#given a square in chess notation, returns a rank and file numbers separated by a space
					#e.g: "a6" = "5 0"
	
		return str(int(square[1]) - 1) + " " + str(fileRead.index(square[0]))


ifChess.main()
