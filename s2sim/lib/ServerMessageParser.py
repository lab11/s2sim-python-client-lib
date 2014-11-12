from ServerMessageBaseClass import ServerMessage
from ServerMessages import *

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