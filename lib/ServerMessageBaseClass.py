class ServerMessage(object):
    """
    Base class for the rest of the server messages
    """
    SetCurrentPriceMsgID = 0x0002
    SysTimeResponseID = 0x0007
    SyncClientConnectionResponseID = 0x0005
    PriceProposalID = 0x0003

    def __init__(self, msg_id, hex_msg):
        self.hex_msg = hex_msg
        self.msg_id = msg_id
        self.unpack_header()
        self.unpack_data()

    def unpack_header(self):
        message = self.hex_msg
        self.server_id = message[4:6].encode("hex")
        self.client_id = message[6:8].encode("hex")
        self.seq_num = int(message[8:12].encode("hex"), 16)
        self.msg_type = message[12:14].encode("hex")
        self.msg_id = message[14:16].encode("hex")
        self.data_size = int(message[16:20].encode("hex"), 16)
        self.data_blob = message[20:-8]

    def unpack_data(self):
        raise NotImplementedError

    def __str__(self):
        return "SERVER MSG: {}\n   Hex: {}\n\n{}\n\n{}".format(self.__class__.__name__, self.hex_str(), self.header_str(), self.data_str())

    def hex_str(self):
        orig_str = binascii.hexlify(self.hex_msg)
        # add nice spacing
        header = "{} {} {} {} {} {} {}".format(orig_str[:8], orig_str[8:12], orig_str[12:16], orig_str[16:24], orig_str[24:28], orig_str[28:32], orig_str[32:40])
        data = self.data_str_hex(orig_str)
        end = orig_str[-8:]
        return header + data + end

    def data_str_hex(self):
        raise NotImplementedError

    def header_str(self):
        s = "   Server ID: {}\n".format(self.server_id)
        s += "   Client ID: {}\n".format(self.client_id)
        s += "   Seq No: {}\n".format(self.seq_num)
        s += "   Msg Type: {}\n".format(self.msg_type)
        s += "   Msg ID: {}\n".format(self.msg_id)
        s += "   Data Size: {}".format(self.data_size)
        return s

    def data_str(self):
        raise NotImplementedError