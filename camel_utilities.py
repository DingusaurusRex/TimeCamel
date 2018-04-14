import camelup as c
import math
import random

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
#def rollDie():

# Randomly choose one of the camels who hasn't moved to move
# output: integer, the camel number to move
#def chooseCamelToMove(gameState)

# Move the given camel (and all camels above it) by the given amount
# output: new gamestate
#def moveCamel(gameState, camel, movement):

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