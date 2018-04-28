# Our Bot
import move
import camel_utilities
from playerinterface import PlayerInterface

# Move Constants
ROLL_MOVE = 0
PLACE_TRAP_MOVE = 1
PLACE_ROUND_BET = 2
PLACE_GAME_WINNER_BET = 3
PLACE_GAME_LOSER_BET = 4

# Trap Constants
MIRAGE = -1
OASIS = 1

ROUND_ITERATIONS_GAME = 1000
ROUND_ITERATIONS_ROUND = 100
TRAP_PLACEMENT_CHANCE = 0

MOVE_EXPECTED_VALUE = 1

gameBetsPlaced = []

class TimeCamel(PlayerInterface):
		
	# Return the expected value of a Roll move
	# output: [move, expected_value]
	def rollExpectedValue(playerNum, gameState):
		m = move.Move(ROLL_MOVE)
		e = MOVE_EXPECTED_VALUE
		return [m, e]
	
	# Return the expected value of a Round Bet move
	# output: [[move, expected value], ...]
	def roundBetExpectedValues(playerNum, gameState):
		result = []
		
		camelPercentages = camel_utilities.randRoundWinnerPercentageTraps(gameState, ROUND_ITERATIONS_ROUND, TRAP_PLACEMENT_CHANCE)
		
		for camelPercentage in camelPercentages:
			camel = camelPercentage[0]
			winPercentage = camelPercentage[1]
			e = camel_utilities.getRoundBetExpectedValue(gameState, camel, winPercentage)
			
			m = move.Move(PLACE_ROUND_BET).withChosenCamel(camel)
			result.append([m, e])
		
		return result
	
	# Return the expected value of a Game Winner Bet move
	# output: [[move, expected value], ...]
	def gameWinnerAndLoserExpectedValues(playerNum, gameState):
		result = []
		
		winners, losers = camel_utilities.randGameWinnersAndLosers(gameState, ROUND_ITERATIONS_GAME, TRAP_PLACEMENT_CHANCE)
		
		for winner in winners:
			camel = winner[0]
			percentage = winner[1]
			
			e = camel_utilities.getWinnerBetExpectedValue(gameState, gameBetsPlaced, camel, percentage)
			m = move.Move(PLACE_GAME_WINNER_BET).withChosenCamel(camel)
			
			result.append([m, e])
		
		for loser in losers:
			camel = loser[0]
			percentage = loser[1]
			
			e = camel_utilities.getLoserBetExpectedValue(gameState, gameBetsPlaced, camel, percentage)
			m = move.Move(PLACE_GAME_LOSER_BET).withChosenCamel(camel)

			#print(str(camel) + str(percentage))
			
			result.append([m, e])
		
		return result
		
	# Get a list of moves and their expected values
	# output: list of [move, expected_value]
	def getMoves(playerNum, gameState):
		moves = []

		#print(TimeCamel.rollExpectedValue(playerNum, gameState))
		
		moves.append(TimeCamel.rollExpectedValue(playerNum, gameState))
		#print(moves)
		moves.extend(TimeCamel.roundBetExpectedValues(playerNum, gameState))
		#print(moves)
		moves.extend(TimeCamel.gameWinnerAndLoserExpectedValues(playerNum, gameState))
		#print(moves)
		# TODO: Add other moves here
		
		return moves
		
	# Determine the move our bot will use
	def move(playerNum, gameState):
		moves = TimeCamel.getMoves(playerNum, gameState)
		
		expectedValue = 0
		
		for move in moves:
			if move[1] > expectedValue:
				result = move[0]
				expectedValue = move[1]
		
		# if game bet, add camel number to gameBetsPlaced
		if result.moveType == PLACE_GAME_WINNER_BET or result.moveType == PLACE_GAME_LOSER_BET:
			gameBetsPlaced.append(result.chosenCamel)
			
		return result.generateMoveArray()