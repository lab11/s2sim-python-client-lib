class ClientMessage(object):
    """
    Base class for the rest of the client messages
    """
    def __init__(self, sender_id, seq_num, msg_type, message_id):
        self.msg_id = message_id
        self.sender_id = sender_id
        self.start_of_message = "12345678"
        self.receiver_id = "0000"
        self.seq_num = seq_num
        self.msg_type = msg_type
        self.end_of_message = "FEDCBA98"

    def to_byte_array(self):
        start_of_message = hex_str_bytes(self.start_of_message)     # 4 bytes
        sender_id = hex_str_bytes(self.sender_id)                   # 2 bytes 0xFFFF is default
        receiver_id = hex_str_bytes(self.receiver_id)               # 2 bytes
        seq_num = int_bytes(self.seq_num)                           # 4 bytes
        msg_type = hex_str_bytes(self.msg_type)                     # 2 bytes
        msg_id = hex_str_bytes(self.msg_id)                         # 2 bytes
        data_size, data = self.get_data_fields()                    # 4 bytes and N bytes
        end_of_message = hex_str_bytes(self.end_of_message)         # 4 bytes
        # construct message
        message = bytearray()
        message += start_of_message
        message += sender_id
        message += receiver_id
        message += seq_num
        message += msg_type
        message += msg_id
        message += data_size
        message += data
        message += end_of_message
        return message

    def get_data_fields(self):
        data_bytes = self.data_to_byte_array()
        unpadded_data_size = len(data_bytes)
        padding = 4 - (unpadded_data_size % 4) if (unpadded_data_size % 4) != 0 else 0
        total_size_hex_str = "{:X}".format(unpadded_data_size + padding)
        while len(total_size_hex_str) < 8:
            total_size_hex_str = "0" + total_size_hex_str
        self.data_size = int(total_size_hex_str, 16)
        total_size = hex_str_bytes(total_size_hex_str)
        padding_remaining = padding
        padded_data = bytearray()
        while padding_remaining > 0:
            padded_data.append(0x00)
            padding_remaining -= 1
        data_bytes = padded_data + data_bytes
        return total_size, data_bytes

    def data_to_byte_array(self):
        raise NotImplementedError

    def __str__(self):
        return "CLIENT MSG: {}\n   Hex: {}\n\n{}\n\n{}".format(self.__class__.__name__, self.hex_str(), self.header_str(), self.data_str())

    def hex_str(self):
        orig_str = binascii.hexlify(self.to_byte_array())
        # add nice spacing
        header = "{} {} {} {} {} {} {}".format(orig_str[:8], orig_str[8:12], orig_str[12:16], orig_str[16:24], orig_str[24:28], orig_str[28:32], orig_str[32:40])
        data = self.data_str_hex(orig_str)
        end = orig_str[-8:]
        return header + data + end

    def data_str_hex(self, hex_str):
        raise NotImplementedError

    def header_str(self):
        s = "   Client ID: {}\n".format(self.sender_id)
        s += "   Server ID: {}\n".format(self.receiver_id)
        s += "   Seq No: {}\n".format(self.seq_num)
        s += "   Msg Type: {}\n".format(self.msg_type)
        s += "   Msg ID: {}\n".format(self.msg_id)
        s += "   Data Size: {}".format(self.data_size)
        return s
        
    def data_str(self):
        raise NotImplementedError