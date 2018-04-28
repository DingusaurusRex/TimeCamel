import camelup as c
import math
import random
import copy
import move
import itertools
import pandas as pd
import numpy as nm

ROUND_BET_VALUES = [5, 3, 2]
GAME_BET_VALUES = [8, 5, 3, 2]

GAME_BET_CORRECT_PERCENTAGE = .25
ROUND_BET_PERCENTAGE_THRESHOLD = 0
GAME_WIN_BET_PERCENTAGE_THRESHOLD = .4
GAME_LOSE_BET_PERCENTAGE_THRESHOLD = .4

# creates a new game state 
# the game state is prepopulated with the moved camels 
def startGame():
	return(c.GameState())

# find the camel on the track 
# input: camel number, current track object (GameState.camel_track)
# output: [board space, spot on stack]
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
	return random.randint(1, 3)

# Randomly choose one of the camels who hasn't moved to move
# output: integer, the camel number to move
def chooseCamelToMove(gameState):
    camelToMove = -1
    camelMoveState = gameState.camel_yet_to_move
    unmovedCamelIndices = []
    for index, camelState in enumerate(camelMoveState):
        if camelState == True:
            unmovedCamelIndices.append(index)
    camelToMove = random.choice(unmovedCamelIndices)
    return camelToMove

	
	# commented out this code - i don't think that it's needed anymore?
	#camelToMove = -1
	#camelMoveState = gameState.camel_yet_to_move
	#unmovedCamelIndices = []
	#for index, camelState in enumerate(camelMoveState):
	#	if camelState == True:
	#		unmovedCamelIndices.append(index)
	#if len(unmovedCamelIndices) < 1:
	#	return -1
	#else:
	#	return random.choice(unmovedCamelIndices)

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
			# for some reason this isn't working - commented out 
			#result.player_money_values[newLocationTrap[1]] += 1
			
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
def moveAllCamels(gameState):
	result = copy.deepcopy(gameState)
	numCamelsToMove = sum(result.camel_yet_to_move)
	for x in range (0, numCamelsToMove):
		camel = chooseCamelToMove(result)
		movement = rollDie()
		result = moveOneCamel(result, camel, movement)
		# TODO:  Check if the game should be over and break
		# stop moving the camels if the game is done 
		if findCamel(camel,result.camel_track)[0] >= 16: 
			result.active_game = False 
			return result 
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
	# seperated for easier reading 
	if not camelLocations[before] and not camelLocations[trapLocation] and not camelLocations[after]:
		if not trapLocations[before] and not trapLocations[trapLocation] and not trapLocations[after]:
			result.trap_track[trapLocation].append(trapType)
			# return the updated gamestate 
			return result
	return None

# Place a bet on the given camel
# output: new gamestate
def placeRoundBet(gameState, camel):
	result = copy.deepcopy(gameState)
	result.round_bets.append(camel)
	return result
	
# Place a bet on the winning camel
# output: new gamestate
def placeWinnerBet(gameState, camel):
	result = copy.deepcopy(gameState)
	result.game_winner_bets.append(camel)
	return result
	
# Place a bet on the losing camel
# output: new gamestate
def placeLoserBet(gameState, camel):
	result = copy.deepcopy(gameState)
	result.game_loser_bets.apend(camel)
	return result

# Execute the move specified on the given game state
def makeMove(gameState, move):
	result = copy.deepcopy(gameState)
	if move.moveType == ROLL_MOVE:
		camel = chooseCamelToMove(result)
		movement = rollDie()
		result = moveOneCamel(result, camel, movement)
	elif move.moveType == PLACE_TRAP_MOVE:
		result = placeTrap(result, move.trapType, move.trapLocation)
	elif move.moveType == PLACE_ROUND_BET:
		result = placeRoundBet(result, move.chosenCamel)
	elif move.moveType == PLACE_GAME_WINNER_BET:
		result = placeWinnerBet(result, move.chosenCamel)
	elif move.moveType == PLACE_GAME_LOSER_BET:
		result = placeLoserBet(result, move.chosenCamel)
	return result
	

# Returns the percentage chance that each camel will win the round, given the current game state
# output: array specifying the round win percent for each camel i.e. [.15, .5, .15, .15, .05]
def roundWinnerPercentages(gameState):
    localGameState = copy.deepcopy(gameState)
    camelOrderPermutations = itertools.permutations(localGameState.camels)
    diceRollOptions = (1, 2, 3)

    # determines number of times a game will end in a given state, given all possible outcomes (excludes trap movement)
    endStatTracker = {}
    for permutation in camelOrderPermutations:
        for roll in diceRollOptions:
            for camel in permutation:
                moveOneCamel(localGameState, camel, roll)
            if localGameState.camel_track in endStatTracker:
                leadCamel = getLeadCamel(localGameState.camel_track)
                endStatTracker[leadCamel] = 0
            endStatTracker[leadCamel] += 1

            # reset gameState
            localGameState = copy.deepcopy(gameState)

# Finds the lead camel from the camel track
# input: the current camel track 
# output: the winning camel [0,1,2,3,4]
def getLeadCamel(camel_track):
	winning_camel = -1
	for l in camel_track:
		if l:
			# get the last in the list
			winning_camel = l[-1]
	return winning_camel

def getLastCamel(camel_track):
	for l in camel_track:
		if l:
			# return the first camel found
			return l[0]

# Return the expected value of a Round Bet on the given camel with the given win percentage
def getRoundBetExpectedValue(gameState, camel, percentage):
	betsPlacedOnCamel = 0
	for bet in gameState.round_bets:
		if bet[0] == camel:
			betsPlacedOnCamel += 1
	#print(gameState.round_bets)
	if betsPlacedOnCamel >= len(ROUND_BET_VALUES):
		return 0
	nextBetValue = ROUND_BET_VALUES[betsPlacedOnCamel]
	losePercentage = 1 - percentage
	if percentage < ROUND_BET_PERCENTAGE_THRESHOLD:
		return 0
	else:
		return nextBetValue * percentage - losePercentage

# Return the expected value of a game winning bet placed on the camel with the percentage it will win
# NOTE:  if a game bet has already been placed on the given camel, expected value is 0
def getWinnerBetExpectedValue(gameState, betsPlaced, camel, percentage):
	if camel in betsPlaced or percentage < GAME_WIN_BET_PERCENTAGE_THRESHOLD:
		return 0
	else:
		numBetsPlaced = len(gameState.game_winner_bets)
		correctBets = min(math.ceil(numBetsPlaced * GAME_BET_CORRECT_PERCENTAGE), 4)
		losePercentage = 1 - percentage
		return GAME_BET_VALUES[correctBets] * percentage - losePercentage

# Return the expected value of a game losing bet placed on the camel with the percentage it will lose
# NOTE:  if a game bet has already been placed on the given camel, expected value is 0
def getLoserBetExpectedValue(gameState, betsPlaced, camel, percentage):
	if camel in betsPlaced or percentage < GAME_LOSE_BET_PERCENTAGE_THRESHOLD:
		return 0
	else:
		numBetsPlaced = len(gameState.game_loser_bets)
		correctBets = min(math.ceil(numBetsPlaced * GAME_BET_CORRECT_PERCENTAGE), 4)
		losePercentage = 1 - percentage
		return GAME_BET_VALUES[correctBets] * percentage - losePercentage

# Removing this methods since you can go this with probability traps = 0 
# in randRoundWinnerPercentageTraps
# Use random permutations to calculate the camel who had the highest percentage
# Note: doesn't take into consideration traps  
# of times in the lead
# input: number of iterations, camel track  
# output: [[camel, percentage],[camel, percentage] ...]
# the last one is the winning camel
# the camel with the highest percentage of time randomally in the lead from this 
# current camel track 
#def randRoundWinnerPercentage(game_state,num_iterations):
	#lead_camels=list()
	#for i in range(0,num_iterations):
	#	g_new=moveAllCamels(game_state)
	#	lead_camels.append(getLeadCamel(g_new.camel_track))
	#leads=pd.Series(lead_camels).value_counts().to_frame().sort_values(by=0)/len(lead_camels)
	#winner=leads.index[leads.shape[0]-1]
	#percentage=leads.values[leads.shape[0]-1]/len(lead_camels)
	#return [winner, float(percentage)]
	#leads=nm.vstack((leads[0].index,leads[0].values)).T.tolist()
	# return all of the percentages 
	#return leads

# Similar to moveCamels but with random trap placements 
def moveAllCamelsTraps(game_state,probability_trap):
	new_game_state=copy.deepcopy(game_state)
	for c in range(0,sum(new_game_state.camel_yet_to_move)):
		# use the probability supplied to determine if the trap should be set 
		if random.random() < probability_trap:
			# randomly select the type and location 
			trap_type=random.sample(k=1,population=[-1,1])[0]
			trap_loc=random.sample(k=1,population=range(0,15))[0]
			# save the new game state 
			tmp_game_state=placeTrap(new_game_state,trap_type,trap_loc)
			# change to the new if the game state is not changed 
			if tmp_game_state is not None:
				new_game_state=tmp_game_state
		# move the camel 
		camel = chooseCamelToMove(new_game_state)
		movement = rollDie()
		new_game_state=moveOneCamel(new_game_state,camel,movement)
		if findCamel(camel,new_game_state.camel_track)[0] >= 16: 
			new_game_state.active_game = False 
			return new_game_state
	return new_game_state


# Similar to randRoundWinnerPercentage except with traps!!! 
# output: [[camel, percentage],[camel, percentage] ...]
def randRoundWinnerPercentageTraps(game_state,num_iterations,probability_trap=0.75):
	lead_camels=list()
	for i in range(0,num_iterations):
		# store a copy of the initial game state 
		new_game_state=moveAllCamelsTraps(game_state,probability_trap)
		# store the lead camel
		lead_camels.append(getLeadCamel(new_game_state.camel_track))
	leads=pd.Series(lead_camels).value_counts().to_frame().sort_values(by=0)/len(lead_camels)
	#winner=leads.index[leads.shape[0]-1]
	#percentage=leads.values[leads.shape[0]-1]/len(lead_camels)
	leads=nm.vstack((leads[0].index,leads[0].values)).T.tolist()
	# return all of the percentages 
	return leads
	#return [winner, float(percentage)]

# Calculate the game winner percentages 
# output: leads: [[camel, percentage],[camel, percentage] ...], 
# 			lasts: [[camel, percentage],[camel, percentage] ...]
def randGameWinnersAndLosers(game_state,num_iterations,probability_traps):
	lead_camels=list()
	last_camels=list()
	for i in range(0,num_iterations):
		new_game_state=copy.deepcopy(game_state)
		rounds=0
		while new_game_state.active_game:
			if probability_traps > 0:
				new_game_state=moveAllCamelsTraps(new_game_state,probability_traps)
			else:
				new_game_state=moveAllCamels(new_game_state)
			new_game_state.camel_yet_to_move=[True,True,True,True,True]
			rounds+=1 
		lead_camels.append(getLeadCamel(new_game_state.camel_track))
		last_camels.append(getLastCamel(new_game_state.camel_track))
	leads=pd.Series(lead_camels).value_counts().to_frame().sort_values(by=0)/len(lead_camels)
	lasts=pd.Series(last_camels).value_counts().to_frame().sort_values(by=0)/len(last_camels)
	#winner=leads.index[leads.shape[0]-1]
	#percentage=leads.values[leads.shape[0]-1]/len(lead_camels)
	#return [winner, float(percentage)]
	leads=nm.vstack((leads[0].index,leads[0].values)).T.tolist()
	lasts=nm.vstack((lasts[0].index,lasts[0].values)).T.tolist()
	# return all of the percentages 
	return leads, lasts