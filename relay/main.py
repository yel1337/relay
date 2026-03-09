from magnet.coil import ElectroMagnet as em
from switch.close import close as c
from switch.open  import open as o
import argparse
import logging
import sys

class RelayException(Exception):
	# 0 if core is not connected with the armature
	# 2 if no current flow 
	def __init__(self, signal):
		self.signal = signal
		self.message = f""

		if self.signal == 0:
			self.message = f"CORE_ERR: NOT CONNECTED WITH ARMATURE "
		elif self.signal == 2:
			self.message = f"CORE_ERR: NO FLOW FROM THE COIL"
	
	def __str__(self):
		return self.message

class CurrentException(RelayException):
	pass
		 
class Main():
	def __init__(self, m, v, r, fc_value):
		self.v_value = v
		self.r_value = r
		self.magnetic = m
		self.armature = 0
		self.fc = fc_value

	def attach(self):
		return self.armature + 1 # 1 is attached to core
	
	def return_spring(self):
		if self.armature == 1:
			return False
		elif self.armature == 0:
			return True # if True then the spring returns the
						# armature
		
	# Once there is a positive magnetic field
	# the core of the coil must be attached
	# with the armature along with the
	# return spring
	def connect_core(self):
		s = self.return_spring()
		if self.magnetic:
			self.attach()
			return True
		elif self.magnetic is False and s:
			raise RelayException(0)
	
	# fc is for NC and NO return value
	# com will depends either to both
	# of the fixed contacts
	def com(self):
		c = 0
		if self.fc:
			return 1 # com connected to NC 
		else:
			return c # as 0 means com connected to NO
	
	def signal_output(self, com):
		if com == 1:
			return f"com_value is {com}, NORMALLY CLOSED"
		elif com == 0:
			return f"com_value is {com}, NORMALLY OPEN"

	def light(self, contact_status):
		# Light can only be turned on if a NC is closed
		# otherwise NO is triggered 
		if contact_status == 1:
			return True
		elif contact_status == 0:
			return False 

	def main(self):
		# Check if armature is connected to the core of the coil
		cc = self.connect_core()
		com_value = self.com()
		if cc is True:
			if com_value == 1:
				pass
		elif cc is False:
			raise RelayException(self.attach)

		# Light Switch
		return f"light status: {self.light(com_value)}"

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# Ex. python relay(10, 3) // 10V and 3r
	parser.add_argument("v", type=int, help='voltage')
	parser.add_argument("r", type=int, help="resistance")
	parser.add_argument(
		'-d', '--debug',
		action='store_true',
		default=False,
		help='Debug COM'
	)
	args = parser.parse_args()

	magnet = em(args.v, args.r)
	current = magnet.current_measurement(args.v, args.r)
	magnetic_field_val = magnet.gen_magnetic(current)
	try:
		if magnetic_field_val is False:
			raise CurrentException()
	except CurrentException as e:
		pass

	relay = Main(em.gen_magnetic, args.v, args.r, True)

	if args.debug:
		print("Debug mode enabled. Printing debug info to stderr.", file=sys.stderr)
		x = print(f"{relay.signal_output(relay.com())}")
		logging.debug(f"{x}")
		logging.basicConfig(level=logging.INFO)
	
	print(relay.main())