class S2SimSession(object):
	sender_id = "FFFF" #aka obj_id, not to be confused w/object name
	obj_name = None

	curr_sys_time = None
	sim_time_step = None
	seq_num = int(0xFFFFFFFF)-1

	sock = None

	def __init__(self, obj_name):
		self.obj_name = obj_name

	def s2sim_connect(self):
		#connected = False
		#attempts = 0
		#wait_sec = 5
		#while not connected:
			#try:
				conn_msg = SyncClientConnectionRequest(self.sender_id, self.seq_num+1, self.obj_name)
				response = self.send_msg(conn_msg)
				#connected = True
				if response.__class__.__name__ == "SyncClientConnectionResponse":
					if response.request_result == 0:
						self.sender_id = response.client_id
						self.seq_num = response.seq_num
					elif response.request_result == 1:
						print("Object ID not found.")
						exit()
				else:
					print("Problem connecting.")
			#except:
			#	attempts += 1
			#	print("Connection attempts: {0}\nSleeping for {1} seconds before retrying." + str(attempts, wait_sec))
			#	sleep(wait_sec)

	def s2sim_disconnect(self):
		print("disconnecting")
		if self.sock != None:
			self.sock.close()

	def report_power(self, power_consumed):
		data_msg = SyncClientData(self.sender_id, self.seq_num+1, power_consumed)
		self.send_async_msg(data_msg)

	def get_time(self):
		time_msg = SystemTimePrompt(self.sender_id, self.seq_num+1)
		response = self.send_msg(time_msg)
		return response

	def get_price(self):
		price_msg = GetPrice(self.sender_id, self.seq_num+1)
		response = self.send_msg(price_msg)
		return response

	def send_demand_negotiation(self, energy_demands):
		demand_msg = DemandNegotiation(self.sender_id, self.seq_num+1, len(energy_demands), energy_demands)
		response = self.send_msg(demand_msg)
		return response

	# blocking receive
	def wait_for_server(self):
		# wait for response
		self.sock.settimeout(60.0)
		connResp = self.sock.recv(BUFFER_SIZE)
		response = parseMessage(connResp)
		self.seq_num += 1
		if s2sim_debug == True:
			print("\n")
			print(response)
		return response

	######################## PRIVATE METHODS #############################

	# synchronous send -- send to server and wait for response
	def send_msg(self, msg):
		self.send_async_msg(msg)
		response = self.wait_for_server()
		return response

	# asynchronous send -- just send to server, no response
	def send_async_msg(self, msg):
		if self.sock == None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((ADDRESS, PORT))
		self.sock.send(msg.to_byte_array())
		self.seq_num += 1
		if s2sim_debug == True:
			print("\n")
			print(msg)