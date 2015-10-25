class Call:
	def __init__(self, call_number, call_datetime):
		self.number = call_number
		self.time = call_datetime

	def get_call_number(self):
		return self.number

	def get_call_time(self):
		return self.time