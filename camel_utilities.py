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
def chooseCamelToMove(gameState)
    camelToMove = -1
    camelMoveState = gamestate.camel_yet_to_move
	
	# get list of camel numbers that haven't moved
	# randomly pick an index of that list
	# return the camel number at that index
	
    unmovedCamels = sum(camelMoveState) - len(camelMoveState)
    if (unmovedCamels == 0):
        return -1
    unmovedCamelChoice = randInt(1, unmovedCamels)
        unmovedCount = 0
        index = 0
    for camel in camelMoveState:
        index += 1
        if camel == False
            unmovedCount += 1
        if unmovedCount == unmovedCamelChoice:
            camelToMove = index
            break
    return camelToMove
        

# Move the given camel (and all camels above it) by the given amount
# output: new gamestate
def moveOneCamel(gameState, camel, movement):
	result = copy.deepcopy(gameState)
	track = result.camel_track
	
	# find camel location
	camelLocation = findCamel(camel, track)
	
	# get camel unit
	camelUnit = track[camelLocation[0]][camelLocation[1]:]
	
	# determine new location
	newLocation = camelLocation[0] + movement
	
	# adjust new location based on traps
	moveBack = false
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
#def moveAllCamels(gameSate):

# Place a bet on the given camel
# output: new gamestate
#def placeRoundBet(gameState, camel):

# Place a bet on the losing camel
# output: new gamestate
#def placeLoserBet(gameState, camel):

# Place a bet on the winning camel
# output: new gamestate
#def placeWinnerBet(gameState, camel):

# Place a trap on the given tile
# output: new gamestate
#def placeTrap(gameState, trapType, trapLocation):
