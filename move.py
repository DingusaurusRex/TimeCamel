# Move Constants
ROLL_MOVE = 0
PLACE_TRAP_MOVE = 1
PLACE_ROUND_BET = 2
PLACE_GAME_WINNER_BET = 3
PLACE_GAME_LOSER_BET = 4

# Trap Constants
MIRAGE = -1
OASIS = 1

moveType = 0
trapType = 0
trapLocation = 0
chosenCamel = 0

def __init__(self, moveType):
	self.moveType = moveType
	
def withTrapType(trapType):
	self.trapType = trapType
	return self
	
def withTrapLocation(trapLocation):
	self.trapLocation = trapLocation
	return self

def withChosenCamel(chosenCamel):
	self.chosenCamel = chosenCamel
	return self
	
def generateMoveArray():
	if moveType == ROLL_MOVE:
		return [ROLL_MOVE]
	elif moveType == PLACE_TRAP_MOVE:
		return [PLACE_TRAP_MOVE, trapType, trapLocation]
	elif moveType == PLACE_ROUND_BET:
		return [PLACE_ROUND_BET, chosenCamel]
	elif moveType == PLACE_GAME_WINNER_BET:
		return [PLACE_GAME_WINNER_BET, chosenCamel]
	elif moveType == PLACE_GAME_LOSER_BET:
		return [PLACE_GAME_LOSER_BET, chosenCamel]
	else:
		return None