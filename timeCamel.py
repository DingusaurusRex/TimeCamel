# Our Bot
import move
import camel_utilities
from playerinterface import PlayerInterface

ROUND_ITERATIONS = 1000

class TimeCamel(PlayerInterface):

	def move(playerNum, gameState):
		moves = getMoves(playerNum, gameState)
		
		expectedValue = 0
		
		for move in moves:
			if move[1] > expectedValue:
				result = move[0]
				expectedValue = move[1]
		
		return result.generateMoveArray()
	
	# Get a list of moves and their expected values
	# output: list of [move, expected_value]
	def getMoves(playerNum, gameState):
		moves = []
		
		moves.append(rollExpectedValue(playerNum, gameState))
		moves.append(roundBetExpectedValue(playerNum, gameState))
		# TODO: Add other moves here
		
		return moves
	
	# Return the expected value of a Roll move
	# output: [move, expected_value]
	def rollExpectedValue(playerNum, gameState):
		m = move(move.ROLL_MOVE)
		e = 1
		return [m, e]
	
	# Return the expected value of a Round Bet move
	# output: [move, expected value]
	def roundBetExpectedValue(playerNum, gameState):
		roundWinner = camel_utilities.randRoundWinnerPercentage(gameState, ROUND_ITERATIONS)
		m = move(move.PLACE_ROUND_BET).setChosenCamel(roundWinner[0])
		e = camel_utilities.getCamelExpectedValue(gameState, roundWinner[0], roundWinner[1])
		return [m, e]