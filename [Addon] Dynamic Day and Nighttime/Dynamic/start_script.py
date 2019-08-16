import Anno6
class Day_Night_Cycle:
	def __init__(self):
		print("day_night_cycle init")
		self.enable = True       # Enabled by Default
		self.speed = 12.0        # Minutes per Day_Night_Cycle
		self.stepping = 9024.0   #   Steps per Day_Night_Cycle
		self.speed = self.speed/10
	def advance(self):
		if(self.enable):
			session.daytime += (24.0/(self.stepping*self.speed))
			game.executeDelayed(int(self.speed*60.0*1000.0/(self.stepping*self.speed)), "day_night_cycle.advance()")	
	def toggle(self):
		self.enable ^= 1
		self.advance()
	def onSessionEnter(self, *args):
		if(self.enable):
			self.enable = False;
			game.executeDelayed(5000, "day_night_cycle.toggle()")
					
day_night_cycle = Day_Night_Cycle();
Anno6.GameEvents.onSessionEnter.append(day_night_cycle.onSessionEnter)
# use day_night_cycle.toggle() to toggle it on and off