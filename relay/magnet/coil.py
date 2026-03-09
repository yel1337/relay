class ElectroMagnet(): 
	def __init__ (self, v, r):
		self.v_value = v
		self.r_value = r

	def current_measurement(self, v, r):
		try:
			from main import CurrentException
			if v > 1 and r > 1:
				return v / r
			else:
				raise CurrentException("amps shoudn't be equal to 0")
		except CurrentException as e:
			pass

	def gen_magnetic(self, current):
		if current:
			return True
		else:
			return False
