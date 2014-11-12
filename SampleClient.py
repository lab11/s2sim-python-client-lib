from s2sim.lib.S2SimSession import S2SimSession #import S2SimSession
from time import sleep
from random import randint
import sys

ADDRESS = 'seelabc.ucsd.edu'
PORT = 26999

# Upon first connection, sender id = 0xFFFF. The sender_id to use for subsequent msgs will
# be scraped from the sender_id field of a successful connection response from the server
new_sender_id = "FFFF"
sender_id = None 

s2sim_debug = False 

def main():
	global s2sim_debug
	if '-d' in sys.argv:
		s2sim_debug = True

	# Contact S2Sim admins to request your own object name.
	obj_name = "UMICH2" 

	session = S2SimSession(obj_name)
	session.s2sim_connect(ADDRESS, PORT)

	try:
		# This loop comprises the logic for a single S2Sim interval
		while(True):

			# Wait for price signal
			interval_price = None
			while(interval_price == None):
				msg = session.wait_for_server()
				if msg != None:
					if msg.__class__.__name__ == "SetCurrentPriceMsg":
						interval_price = msg.price_values[0]
				else:
					"Connection closed unexpectedly."
					exit()

			# Do something with the price signal
			normal_energy_demand = 3000 + randint(-20, 20)
			curtailed_energy_demand = 1000 + randint(-20, 20)
			threshold_price = 290 + randint(-20, 20)
			if interval_price > threshold_price:
				print("Price too high. Curtailed load.")
				energy_demand = curtailed_energy_demand 
			elif interval_price <= threshold_price:
				print("Price low. Normal load.")
				energy_demand = normal_energy_demand

			# Report energy demand
			session.report_power(energy_demand)
			report_str = "S2Sim Price: {0}\nThreshold Price: {1}\nEnergy Demand: {2}\n"
			print(report_str.format(interval_price, threshold_price, energy_demand)) 
			sleep(1)

	except KeyboardInterrupt:
		print("\n\nExiting...")
		session.s2sim_disconnect()
		exit()

if __name__=="__main__":
	main()