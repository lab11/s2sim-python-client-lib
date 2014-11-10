def parseMessage(message):
    parsed_msg = None
    #print_bytearray(message)
    has_msg_id = False
    try:
        msg_id = int(message[14:16].encode("hex"), 16)
        has_msg_id = True
    except:
        print("\n\nUnexpected message of length {}".format(len(message)))
        print("Message: "),
        print_bytearray(message)
        print("\n")
        

    if has_msg_id:
        if msg_id == ServerMessage.SysTimeResponseID:
            parsed_msg = SysTimeResponse(message)
        elif msg_id == ServerMessage.SyncClientConnectionResponseID:
            parsed_msg = SyncClientConnectionResponse(message)
        elif msg_id == ServerMessage.SetCurrentPriceMsgID:
            parsed_msg = SetCurrentPriceMsg(message)
        elif msg_id == ServerMessage.PriceProposalID:
            parsed_msg = PriceProposal(message)
        else:
            print("unknown message")

    return parsed_msg




######################## SERVER MESSAGES ###########################

class SyncClientConnectionResponse(ServerMessage):
    request_result = None
    current_sys_time = None
    num_clients = None
    system_mode = None
    sim_time_step_seconds = None

    def __init__(self, hex_msg):
        super(SyncClientConnectionResponse, self).__init__(ServerMessage.SyncClientConnectionResponseID, hex_msg)

    def unpack_data(self):
        message = self.hex_msg
        self.request_result = int(message[20:24].encode("hex"), 16)
        self.current_sys_time = int(message[24:28].encode("hex"), 16)
        self.num_clients = int(message[28:30].encode("hex"), 16)
        self.system_mode = int(message[30:32].encode("hex"), 16)
        self.sim_time_step_seconds = int(message[32:36].encode("hex"), 16)

    def data_str_hex(self, hex_str):
        s = " {} {} {} ".format(hex_str[40:48], hex_str[48:56], hex_str[56:60])
        s += "{} {} ".format(hex_str[60:64], hex_str[64:72])
        return s

    def data_str(self):
        s = "   Request Result: {}\n".format(self.request_result)
        s += "   Current System Time: {}\n".format(self.current_sys_time)
        s += "   Number of Clients: {}\n".format(self.num_clients)
        s += "   System Mode: {}\n".format(self.system_mode)
        s += "   Simulation Time Step: {}\n".format(self.sim_time_step_seconds)
        return s

class PriceProposal(ServerMessage):
    price_interval_begin = None
    num_price_points = None
    price_values = None

    def __init__(self, hex_msg):
        super(PriceProposal, self).__init__(ServerMessage.PriceProposalID, hex_msg)

    def unpack_data(self):
        blob = self.data_blob
        self.price_interval_begin = int(blob[0:4].encode("hex"), 16)
        self.num_price_points = int(blob[4:8].encode("hex"), 16)
        base_index = 8 
        for n in range(self.num_price_points):
            self.price_values.append(int(blob[base_index+(4*n):base_index+(4*(n+1))].encode("hex"), 16))

    def data_str_hex(self, hex_str):
        return " {} {} {} ".format(hex_str[40:48], hex_str[48:56], hex_str[56:56+self.num_price_points*8])

    def data_str(self):
        s = "   Num Price Points: {}\n".format(self.num_price_points)
        s += "   Price Interval Begin: {}\n".format(self.price_interval_begin)
        s += "   Price Values: {}".format(self.price_values)
        return s

class SetCurrentPriceMsg(ServerMessage):
    price_interval_begin = None
    num_price_points = None
    price_values = None

    def __init__(self, hex_msg):
        super(SetCurrentPriceMsg, self).__init__(ServerMessage.SetCurrentPriceMsgID, hex_msg)

    def unpack_data(self):
        message = self.hex_msg
        self.price_interval_begin = int(message[20:24].encode("hex"), 16)
        self.num_price_points = int(message[24:28].encode("hex"), 16)
        i = 28
        self.price_values = []
        for n in range(self.num_price_points):
            try:
                self.price_values.append(int(message[i+(4*n):i+(4*(n+1))].encode("hex"), 16))
            except:
                print(message[i+(4*n):i+(4*(n+1))].encode("hex"))

    def data_str_hex(self, hex_str):
        return " {} {} {} ".format(hex_str[40:48], hex_str[48:56], hex_str[56:56+self.num_price_points*8])

    def data_str(self):
        s = "   Price Interval Begin: {}\n".format(self.price_interval_begin)
        s += "   Num Price Points: {}\n".format(self.num_price_points)
        s += "   Price Values: {}".format(self.price_values)
        return s

class SysTimeResponse(ServerMessage):
    current_sys_time = None

    def __init__(self, hex_msg):
        super(SysTimeResponse, self).__init__(ServerMessage.SysTimeResponseID, hex_msg)

    def unpack_data(self):
        message = self.hex_msg
        self.current_sys_time = int(message[20:24].encode("hex"), 16)

    def data_str_hex(self, hex_str):
        return " {} ".format(hex_str[40:48])

    def data_str(self):
        return "   Time: {}".format(self.current_sys_time)

