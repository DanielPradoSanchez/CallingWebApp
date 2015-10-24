class Call:
	def __init__(self, call_number, call_datetime, call_content):
		self.number = call_number
		self.time = call_datetime
		self.content = call_content

	def get_call_number(self):
		return self.number

	def get_call_time(self):
		return self.time

	def get_call_content(self):
		return self.content