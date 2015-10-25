
from call import Call

class CallList:
	def __init__(self):
		self.calls = []

	def appendCall(self, call_number, call_datetime):
		newCall = Call(call_number, call_datetime)
		self.calls.append(newCall)

	def getCalls(self):
		return self.calls
