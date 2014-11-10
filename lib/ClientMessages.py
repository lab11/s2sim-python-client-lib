import array
import socket
from Utilities import hex_str_bytes, int_bytes, print_bytearray
import binascii


######################### CLIENT MESSAGES ############################

class SyncClientConnectionRequest(ClientMessage):
    """
    Object Name (4xN+R bytes): Identifying name of client. Character string, no NULL termination.
    Padding (4-R bytes): Padd object name with 0x00 to make length a multiple of 4 bytes.
    """
    msg_type = "0001"
    msg_id = "0004"
    def __init__(self, sender_id, seq_num, obj_name):
        super(SyncClientConnectionRequest, self).__init__(sender_id, seq_num, self.msg_type, self.msg_id)
        self.obj_name = obj_name
        self.padding = self.get_padding()

    def get_padding(self):
        amt = 4 - (len(self.obj_name) % 4) if (len(self.obj_name) % 4) != 0 else 0
        padding = bytearray()
        for i in range(amt):
            padding.append(0x00)
        return padding

    def data_to_byte_array(self):
        data = bytearray()
        data += self.obj_name
        data += self.padding
        return data

    def data_str_hex(self, hex_str):
        return " {} {} ".format(hex_str[40:len(self.obj_name)*8], hex_str[len(self.obj_name)*8:-8])

    def data_str(self):
        s = "   Object Name: {}\n".format(self.obj_name)
        s += "   Padding: {}".format(self.padding)
        return s

class SystemTimePrompt(ClientMessage):
    """
    Empty, this is just a message type that will prompt a response.
    """
    msg_type = "0001"
    msg_id = "0006"
    def __init__(self, sender_id, seq_num):
        super(SystemTimePrompt, self).__init__(sender_id, seq_num, self.msg_type, self.msg_id)

    # empty payload
    def data_to_byte_array(self):
        return bytearray()

    def data_str_hex(self, hex_str):
        return " "

    def data_str(self):
        return ""

class GetPrice(ClientMessage):
    """
    Empty, this is just a message type that will prompt a response.
    """
    msg_type = "0003"
    msg_id = "0001"
    def __init__(self, sender_id, seq_num):
        super(GetPrice, self).__init__(sender_id, seq_num, self.msg_id, self.msg_id)

    # empty payload
    def data_to_byte_array(self):
        return bytearray()

    def data_str_hex(self, hex_str):
        return " "

    def data_str(self):
        return ""

class DemandNegotiation(ClientMessage):
    """
    Number of Energy Points (4 bytes): Number of N points in the rest of the message.
    Energy Demand (Nx4 bytes): Amount of energy that will probably be demanded for given price interval.
    """
    msg_type = "0003"
    msg_id = "0004"
    def __init__(self, sender_id, seq_num, num_energy_points, energy_demand):
        super(DemandNegotiation, self).__init__(sender_id, seq_num, self.msg_type, self.msg_id)
        self.num_energy_points = num_energy_points
        self.energy_demand = energy_demand

    def data_to_byte_array(self):
        data = bytearray()
        data += int_bytes(self.num_energy_points)
        for demand in self.energy_demand:
            data += int_bytes(demand)
        return data

    def data_str_hex(self, hex_str):
        return " {} {} ".format(hex_str[40:48], hex_str[48:self.num_energy_points*8])

    def data_str(self):
        s = "   Number of Energy Points: {}\n".format(self.num_energy_points)
        s += "   Energy Demand: {}".format(self.energy_demand)
        return s

class SyncClientData(ClientMessage):
    """
    Energy Demand (4 bytes): Energy actually consumed by client.
    """
    msg_type = "0003"
    msg_id = "0005"
    def __init__(self, sender_id, seq_num, energy_demand):
        super(SyncClientData, self).__init__(sender_id, seq_num, self.msg_type, self.msg_id)
        self.energy_demand = energy_demand

    def data_to_byte_array(self):
        data = bytearray()
        data += int_bytes(self.energy_demand)
        return data

    def data_str_hex(self, hex_str):
        return " {} ".format(hex_str[40:48])

    def data_str(self):
        s = "   Energy Demand: {}".format(self.energy_demand)
        return s
