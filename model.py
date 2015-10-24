
from call import Call

class CallList:
	def __init__(self):
		self.calls = []

	def appendCall(self, call_number, call_datetime, call_content):
		newCall = Call(call_number, call_datetime, call_content)
		self.calls.append(newCall)

	def cancelAllCalls(self):
		del self.calls[:]
		return calls

	def cancelCall(self, call):
		self.calls.remove(call)

	def getCalls(self):
		return self.calls
