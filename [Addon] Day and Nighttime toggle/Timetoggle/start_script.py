class Day_Night:
	def __init__(self):
		print("day_night_cycle init")
	def advance(self, h):
		print('advanced 4h')
		session.daytime = session.daytime + h;
		
			
day_night = Day_Night();
