import time

import chess

import chess.engine

import ioDriver

class chessEngine:
	def __init__(self, GAMEMODE, CPU_DIFFICULTY):
		self.board = chess.Board()
		self.GAMEMODE = GAMEMODE
		self.resignFlag = False
		self.engine = chess.engine.SimpleEngine.popen_uci('src/stockfish')
		self.engine.configure({"Skill Level": CPU_DIFFICULTY})
		self.moveLog = []
		self.whiteTurn = True
		if(GAMEMODE == 'B'):
			self.whiteTurn == False

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

	def pushCPUMove(self):
		CPUMove = self.engine.play(self.board, chess.engine.Limit(time=0.1))
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

	def isLegal(self, UCIMove):
		print("UCI Move: ", end='')
		print(UCIMove)
		move = chess.Move.from_uci(UCIMove)
		if(move in self.board.legal_moves):
			return True
		else:
			return False

	def getMoveLog(self):
		logString = ''
		for move in range(len(self.moveLog)):
			logString = logString + self.moveLog[move]
		return logString

	def getLastMove(self):
		if(len(self.moveLog) > 0):
			return self.moveLog[len(self.moveLog)-1]
		else:
			pass

	def getWinner(self):
		if(self.whiteTurn):
			return 'Black'
		else:
			return 'White'

	def quitEngine(self):
		self.engine.quit()
