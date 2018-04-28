# Move Constants
ROLL_MOVE = 0
PLACE_TRAP_MOVE = 1
PLACE_ROUND_BET = 2
PLACE_GAME_WINNER_BET = 3
PLACE_GAME_LOSER_BET = 4

# Trap Constants
MIRAGE = -1
OASIS = 1

class Move:

	def __init__(self, moveType):
		self.moveType = moveType
		self.trapType = 0
		self.trapLocation = 0
		self.chosenCamel = 0

		
	def withTrapType(self, trapType):
		self.trapType = trapType
		return self
		
	def withTrapLocation(self, trapLocation):
		self.trapLocation = trapLocation
		return self

	def withChosenCamel(self, chosenCamel):
		self.chosenCamel = int(chosenCamel)
		return self
		
	def generateMoveArray(self):
		if self.moveType == ROLL_MOVE:
			return [ROLL_MOVE]
		elif self.moveType == PLACE_TRAP_MOVE:
			return [PLACE_TRAP_MOVE, self.trapType, self.trapLocation]
		elif self.moveType == PLACE_ROUND_BET:
			return [PLACE_ROUND_BET, self.chosenCamel]
		elif self.moveType == PLACE_GAME_WINNER_BET:
			return [PLACE_GAME_WINNER_BET, self.chosenCamel]
		elif self.moveType == PLACE_GAME_LOSER_BET:
			return [PLACE_GAME_LOSER_BET, self.chosenCamel]
		else:
			return None