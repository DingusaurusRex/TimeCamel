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

# move the camel
# input: current game state
#def moveCamel(game)

#def placeRoundBet(camel)

#def placeLoserBet(camel)

#def placeWinnerBet(camel)

#def placeTrap(camel,type)