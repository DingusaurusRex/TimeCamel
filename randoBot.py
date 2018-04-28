# Our Random Bot (for testing)
#   [0] : Move Camel
#   [1,trap_type,trap_location] : Place Trap
#   [2,projected_round_winner] : Make Round Winner Bet
#   [3,projected_game_winner] : Make Game Winner Bet
#   [4,projected_game_loser] : Make Game Loser Bet
import random
import move
import camel_utilities
from playerinterface import PlayerInterface

class RandoBot(PlayerInterface):

    # tracks available game winner/loser cards through turns
    availableGameWinnerLoserCards = [0, 1, 2, 3, 4]
    
    def findPlaceableLocations(gameState, randTrapType):
        placeableLocations = []
        for location in range(15):
            if (camel_utilities.placeTrap(gameState, randTrapType, location) is not None):
                placeableLocations.append(location)
        return placeableLocations
    

    def move(playerNum, gameState):
        possibleMoveTypes = [0, 1, 2, 3, 4]

        # determinize randomized trap type
        randTrapType = random.sample(k=1,population=[-1,1])[0]  

        # determine randomized trap location
        placeableLocations = []
        randTrapLocation = -1
        placeableLocations = RandoBot.findPlaceableLocations(gameState, randTrapType)
        if (len(placeableLocations) > 0):
            randTrapLocation = random.sample(k=1, population=placeableLocations)[0]
        else:
            # remove place trap from possible move types if no possible locations
            possibleMoveTypes.remove(1)

        if (len(RandoBot.availableGameWinnerLoserCards) <= 0):
            # removes make game winner/loser bet from possible move types if no cards left
            possibleMoveTypes.remove(3)
            possibleMoveTypes.remove(4)


        # chooses random move type from remaining possible move types
        randMoveType = random.sample(k=1, population=possibleMoveTypes)[0]
        randProjectedCamel = random.randint(1, 5)

        if randMoveType == move.PLACE_ROUND_BET:
            # determines possible round winning camels that can be chosen and chooses one at random
            initialRandProjectedCamel = randProjectedCamel
            unacceptableCamelBet = True
            while unacceptableCamelBet:
                projectedCamelCount = 0
                for bet in gameState.round_bets:
                    if (bet[0] == randProjectedCamel):
                        projectedCamelCount += 1
                if (projectedCamelCount >= 3):
                    randProjectedCamel += 1
                    if randProjectedCamel > 4:
                        randProjectedCamel = 0
                    if (randProjectedCamel == initialRandProjectedCamel):
                        # removes make round winner bet from possible move types if no cards left
                        possibleMoveTypes.remove(2)
                        # this is bad and a shortcut. Should iterate through and randomly choose move type
                        randMoveType += random.sample(k=1, population=[1, 2])[0] 
                        break
                else:
                    unacceptableCamelBet = False

        if (randMoveType == move.PLACE_GAME_WINNER_BET or randMoveType == move.PLACE_GAME_LOSER_BET):
            initialRandProjectedCamel = randProjectedCamel
            unacceptableCamelBet = True
            while (unacceptableCamelBet):
                if (randProjectedCamel in RandoBot.availableGameWinnerLoserCards):
                    unacceptableCamelBet = False
                else:
                    randProjectedCamel += 1
                    if randProjectedCamel > 4:
                        randProjectedCamel = 0
                    if (randProjectedCamel == initialRandProjectedCamel):
                        possibleMoveTypes.remove(3)
                        possibleMoveTypes.remove(4)
                        randMoveType = random.sample(k=1, population=possibleMoveTypes)[0]
                        break


        myMove = move.Move(randMoveType).withTrapType(randTrapType).withTrapLocation(randTrapLocation).withChosenCamel(randProjectedCamel)
        return myMove.generateMoveArray()
