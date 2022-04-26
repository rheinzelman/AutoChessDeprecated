import time

import chess

import chess.engine

import ioDriver

import platform

'''
GAMEMODE: currently does nothing other than help the chessEngine object keep track of whose turn it is for endgame purposes
CPU_DIFFICULTY: edits stockfish's config file to change difficulty
STARTING_FEN: leave blank for standard FEN, fill with custom FEN otherwise
'''
class chessEngine:
	def __init__(self, GAMEMODE, CPU_DIFFICULTY, STARTING_FEN):

		if('Linux' in platform.system()):
			linux = True
		else:
			linux = False

		#if the starting_fen is empty, then initialize with a standard board fen
		if(not STARTING_FEN):
			self.board = chess.Board()
		#else initialize with the given fen
		else:
			self.board = chess.Board(STARTING_FEN)
		self.GAMEMODE = GAMEMODE
		self.resignFlag = False
		if(linux):
			self.engine = chess.engine.SimpleEngine.popen_uci('src_linux/stockfish/')
		else:
			self.engine = chess.engine.SimpleEngine.popen_uci('src/stockfish')
		self.engine.configure({"Skill Level": CPU_DIFFICULTY})
		self.moveLog = []
		self.whiteTurn = True
		if(GAMEMODE == 'B'):
			self.whiteTurn == False

	#take a UCIMove string in and convert it to chess.Move.from_uci format
	#test it's legality, if it's legal, push and return True, otherwise return false
	#additionally, add the move to the moveLog list 
	def pushPlayerMove(self, UCIMove):
		isLegalMove = False
		print('Your move: ' + UCIMove)
		move = chess.Move.from_uci(UCIMove)
		if(move in self.board.legal_moves):
			isLegalMove = True
			self.board.push(move)
			print(self.board)

			if(len(self.moveLog) == 0):
				self.moveLog.append(str(UCIMove))
			else:
				temp = self.moveLog[len(self.moveLog)-1]
				self.moveLog[len(self.moveLog)-1] = temp + ', '
				self.moveLog.append(str(UCIMove))
			self.whiteTurn = not self.whiteTurn
			return True
		else:
			return False

	#generate a legal cpu move and push it
	#if no moves can be made return false, ending the game vs CPU
	#additionally, add the move to the moveLog list
	def pushCPUMove(self):
		CPUMove = self.engine.play(self.board, chess.engine.Limit(time=0.1))
		if(CPUMove.move in self.board.legal_moves):
			time.sleep(.5)
			print('CPU move: ', end='')
			print(CPUMove.move)
			self.board.push(CPUMove.move)
			print(self.board)
			if(len(self.moveLog) == 0):
				self.moveLog.append(str(CPUMove.move))
			else:
				temp = self.moveLog[len(self.moveLog)-1]
				self.moveLog[len(self.moveLog)-1] = temp + ', '
				self.moveLog.append(str(CPUMove.move))
			self.whiteTurn = not self.whiteTurn
			return True
		else:
			return False

	#takes in a player move and returns true if the player is attempting to move a pawn
	#useful for pawn promotion
	def isPawn(self, playerMove):
		if(self.board.piece_type_at(chess.square(ord(playerMove[0])-97,playerMove[1]-1)) == 1):
			return True
		else:
			return False

	#return moveLog
	def getMoveLog(self):
		logString = ''
		for move in range(len(self.moveLog)):
			logString = logString + self.moveLog[move]
		return logString

	#get the last move of the moveLog
	def getLastMove(self):
		if(len(self.moveLog) > 0):
			return self.moveLog[len(self.moveLog)-1]
		else:
			pass

	#get the current turn of the board
	def getTurn(self):
		if(self.whiteTurn):
			return 'White'
		else:
			return 'Black'
	#get the winner of the last move (simply the not of getTurn)
	def getWinner(self):
		if(self.whiteTurn):
			return 'Black'
		else:
			return 'White'

	#quit the stockfish engine so your computer doesn't explode
	def quitEngine(self):
		self.engine.quit()