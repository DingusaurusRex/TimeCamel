import camelup as c
import math
import random
import copy

# creates a new game state 
# the game state is prepopulated with the moved camels 
def startGame():
    return(c.GameState())

# find the camel on the track 
# input: camel number, current track object (GameState.camel_track)
def findCamel(camel,track):
    no_camel=False
    for s1 in range(0,len(track)):
        if len(track[s1]) > 0:
            for s2 in range(0,len(track[s1])):
                if track[s1][s2] == camel:
                    return [s1,s2]
    if no_camel:
        return [-1,-1]
		
# Randomly pick a number between 1 and 3 inclusive
# output: integer
def rollDie():
    return randInt(1, 3)

# Randomly choose one of the camels who hasn't moved to move
# output: integer, the camel number to move
def chooseCamelToMove(gameState):
    camelToMove = -1
    camelMoveState = gamestate.camel_yet_to_move
    unmovedCamelIndices = []
    for index camelState in enumerate(camelMoveState):
        if camelState == True:
            unmovedCamelIndices.append(index)
    camelToMove = random.choice(unmovedCamelIndices)
    return camelToMove

# Move the given camel (and all camels above it) by the given amount
# output: new gamestate
def moveOneCamel(gameState, camel, movement):
	result = copy.deepcopy(gameState)
	
	# mark the camel as moved
	result.camel_yet_to_move[camel] = False
	
	track = result.camel_track
	
	# find camel location
	camelLocation = findCamel(camel, track)
	
	# get camel unit
	camelUnit = track[camelLocation[0]][camelLocation[1]:]
	
	# determine new location
	newLocation = camelLocation[0] + movement
	
	# adjust new location based on traps
	moveBack = False
	trapTrack = result.trap_track
	if newLocation < len(trapTrack):
		newLocationTrap = trapTrack[newLocation]
		
		# if there is a trap
		if len(newLocationTrap) > 0:
			# adjust the newLocation
			newLocation += newLocationTrap[0]
			
			# add a point to the player who's trap it is
			result.player_money_values[newLocationTrap[1]] += 1
			
			# mark whether we moved back
			moveBack = newLocationTrap[0] == -1
	
	# remove each camel from the old location
	for camel in camelUnit:
		result.camel_track[camelLocation[0]].remove(camel)
	
	# add each camel to the new location
	if newLocation < len(track):
		for camel in camelUnit:
			if moveBack:
				result.camel_track[newLocation].insert(0, camel)
			else:
				result.camel_track[newLocation].append(camel)
	else:
		result.camel_track[len(track)] = camelUnit
		
	return result

# Execute a single round of movement (move all camels once)
# Moves the camels in a random order
# output: new gamestate
def moveAllCamels(gameSate):
	result = copy.deepcopy(gameState)
	numCamelsToMove = sum(result.camel_yet_to_move)
	for x in range (0, numCamelsToMove):
		camel = chooseCamelToMove(result)
		movement = rollDie()
		result = moveOneCamel(result, camel, movement)
	return result

# Place a bet on the given camel
# output: new gamestate
def placeRoundBet(gameState, camel):
	result = copy.deepcopy(gameState)
    result.round_bets.append(camel)
	return result

# Place a bet on the losing camel
# output: new gamestate
def placeLoserBet(gameState, camel):
	result = copy.deepcopy(gameState)
    result.game_loser_bets.apend(camel)
	return result
	
# Place a bet on the winning camel
# output: new gamestate
def placeWinnerBet(gameState, camel):
	result = copy.deepcopy(gameState)
    result.game_winner_bets.append(camel)
	return result

# Place a trap on the given tile
# output: new gamestate
# returns none if trap can not be placed
def placeTrap(gameState, trapType, trapLocation):
    result = copy.deepcopy(gameState)
    before = trapLocation - 1
    after = trapLocation + 1
    camelLocations = result.camel_track
    trapLocations = result.trap_track
    if not camelLocation[before] and not camelLocations[trapLocation] and not camelLocations[after] \
    and  trapLocations[before] and not trapLocations[trapLocation] and not trapLocations[after]
        result.trap_track[trapLocation].append(trapType)
        return result.trap_track[trapLocation].append(trapType)
    return None
