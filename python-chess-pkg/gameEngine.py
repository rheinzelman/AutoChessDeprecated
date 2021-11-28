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
			return False

	def pushCPUMove(self):
		CPUMove = self.engine.play(self.board, chess.engine.Limit(time=0.1))
		time.sleep(.5)
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

