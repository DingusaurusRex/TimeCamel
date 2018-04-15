import camel_utilities as utils

def runAllTests():
	startGame_when_startGame_then_nonNullGameState()
	rollDie_when_rollDie_then_validNumber()
	findCamel_when_singleCamelOnSpace_then_findsCamel()
	findCamel_when_multipleCamelsOnSpace_then_findsCamels()
	chooseCamelToMove_when_choosingCamels_then_choosesCamels()
	print("All Tests Run")
	
def startGame_when_startGame_then_nonNullGameState():
	print("Running startGame_when_startGame_then_nonNullGameState")
	gameState = utils.startGame()
	if gameState == None:
		print("ERROR - startGame_when_startGame_then_nonNullGameState: gameState == None")
		
def rollDie_when_rollDie_then_validNumber():
	print("Running rollDie_when_rollDie_then_validNumber")
	for x in range(0, 10):
		value = utils.rollDie()
		if value < 1 or value > 3:
			print("ERROR - rollDie_when_rollDie_then_validNumber: invalid dice roll " + value)
			return
			
def findCamel_when_singleCamelOnSpace_then_findsCamel():
	print("Running findCamel_when_singleCamelOnSpace_then_findsCamel")
	g = utils.startGame()
	g.camel_track = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	g.camel_track[2].append(42)
	camelLocation = utils.findCamel(42, g.camel_track)
	if camelLocation[0] != 2 or camelLocation[1] != 0:
		print("ERROR - findCamel_when_singleCamelOnSpace_then_findsCamel: incorrect camel location " + str(camelLocation))
		
def findCamel_when_multipleCamelsOnSpace_then_findsCamels():
	print("Running findCamel_when_multipleCamelsOnSpace_findsCamels")
	g = utils.startGame()
	g.camel_track = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	g.camel_track[2].append(1)
	g.camel_track[2].append(2)
	camel1Location = utils.findCamel(1, g.camel_track)
	if camel1Location[0] != 2 or camel1Location[1] != 0:
		print("ERROR - findCamel_when_multipleCamelsOnSpace_then_findsCamels: incorrect camel 1 location " + str(camel1Location))
	camel2Location = utils.findCamel(2, g.camel_track)
	if camel2Location[0] != 2 or camel2Location[1] != 1:
		print("ERROR - findCamel_when_multipleCamelsOnSpace_then_findsCamels: incorrect camel 2 location " + str(camel2Location))
		
def chooseCamelToMove_when_choosingCamels_then_choosesCamels():
	print("Running chooseCamelToMove_when_choosingCamels_then_choosesCamels")
	g = utils.startGame()
	chosenCamels = []
	for x in range (0, 5):
		camel = utils.chooseCamelToMove(g)
		if camel == -1:
			print("ERROR - chooseCamelToMove_when_choosingCamels_then_choosesCamels: unable to find camel when it should")
			return
		if camel in chosenCamels or not g.camel_yet_to_move[camel]:
			print("ERROR - chooseCamelToMove_when_choosingCamels_then_choosesCamels: camel already chosen")
			return
		else:
			chosenCamels.append(camel)
			g.camel_yet_to_move[camel] = False
	camel = utils.chooseCamelToMove(g)
	if camel != -1:
		print("ERROR - chooseCamelToMove_when_choosingCamels_then_choosesCamels: found a camel when it shouldn't "+ str(camel))