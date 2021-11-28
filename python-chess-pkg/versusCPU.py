import time

import chess

import chess.engine

import ioDriver

class CPUClass:
	def __init__(self, playerColor):
		self.board = chess.Board()
		self.playerColor = playerColor
		self.resignFlag = False
		self.engine = chess.engine.SimpleEngine.popen_uci('src/stockfish')

	def pushPlayerMove(self, UCIMove):
		isLegalMove = False
		print('Your move: ' + UCIMove)
		move = chess.Move.from_uci(UCIMove)
		if(move in self.board.legal_moves):
			isLegalMove = True
			self.board.push(move)
			print(self.board)
			return True
		else:
			print('Illegal move!')
			return False

	def pushCPUMove(self):
		CPUMove = self.engine.play(self.board, chess.engine.Limit(time=0.1))
		time.sleep(.35)
		print('CPU move: ', end='')
		print(CPUMove.move)
		self.board.push(CPUMove.move)
		print(self.board)

	def isLegal(self, UCIMove):
		print("UCI Move: ", end='')
		print(UCIMove)
		move = chess.Move.from_uci(UCIMove)
		if(move in self.board.legal_moves):
			return True
		else:
			return False

