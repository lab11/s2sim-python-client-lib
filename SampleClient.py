from S2SimSession import S2SimSession
from time import sleep
import sys

ADDRESS = 'seelabc.ucsd.edu'
PORT = 26999
BUFFER_SIZE = 1024

# Upon first connection, sender id = 0xFFFF. The sender_id to use for subsequent msgs will
# be scraped from the sender_id field of a successful connection response from the server
new_sender_id = "FFFF"
sender_id = None

threshold_price = 300 

s2sim_debug = False 

def main():
	global s2sim_debug
	if '-d' in sys.argv:
		s2sim_debug = True

	# Contact S2Sim admins to request your own object name.
	obj_name = "UMICH2" 

	session = S2SimSession(obj_name)
	session.s2sim_connect()

	try:
		# This loop comprises the logic for a single S2Sim interval
		while(True):

			# Wait for price signal
			price_set = False
			interval_price = None
			while(not price_set):
				msg = session.wait_for_server()
				if msg != None:
					if msg.__class__.__name__ == "SetCurrentPriceMsg":
						interval_price = msg.price_values[0]
						price_set = True
				else:
					"Connection closed unexpectedly."
					exit()

			# Do something with the price signal
			normal_energy_demand = 3000
			curtailed_energy_demand = 1000
			if interval_price > threshold_price:
				print("Price threshold exceeded. Shedding load.")
				energy_demand = curtailed_energy_demand
			elif interval_price <= threshold_price:
				print("Price lowered. Restoring load.")
				energy_demand = normal_energy_demand

			# Report energy demand
			session.report_power(energy_demand)
			sleep(1)

	except KeyboardInterrupt:
		print("\n\nExiting...")
		session.s2sim_disconnect()
		exit()


if __name__=="__main__":
	main()