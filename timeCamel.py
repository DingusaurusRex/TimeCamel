# Our Bot
import move
from playerinterface import PlayerInterface

class TimeCamel(PlayerInterface):

	def move(playerNum, gameState):
		m = move(move.ROLL_MOVE)
		return m.generateMoveArray()