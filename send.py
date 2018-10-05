import pickle
import socket
import time
import os
import random

EstimatedRTT = 500
DevRTT = 250
global buf
buf = 2048

TimeoutInterval = EstimatedRTT + 4*DevRTT

IP_Address = "127.0.0.1"
Port_Address = 5000



class STPPacket:
    def __init__(self, data, seq_num, ack_num, ack, syn, fin):
        self.data = data
        self.seq_num = seq_num
        self.ack_num = ack_num
        # following 3 are all boolean flags
        self.ack = ack
        self.syn = syn
        self.fin = fin

    def setSequenceNumber(self, num):
        print("testing")

    def setAckFlag(self, ack):
        print("Ack Flags")

    def setSynFlag(self, syn):
        print("Syn Flags")

    def setFinFlag(self, fin):
        print("Fin Flags")

    def updateAckNum(self, ack):
        #boolean
        print("boolean fin flag")


class Sender:
    def __init__(self, ip, port, file_name, MWS, MSS, gamma, pDroppDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed):
        self.ip = ip
		self.port = port
		self.file_name = file_name
		self.MWS = int(MWS)
		self.MSS = int(MSS)
		self.timeout = int(timeout)
		self.pDrop = float(pDrop)
		self.pDuplicate = float(pDuplicate
		self.pCorrupt = float(pCorrupt)
		self.maxOrder = float(maxOrder)
		self.pOrder = float(pOrder)
		self.pDelay = float(pDelay)
		self.seed = int(seed)
		self.curr_time = 0
		self.prev_time = 0
		self.start_time = 0

class PLD:
	def __init__(self, pDrop, pDuplicate, pError, pOrder, pDelay):
		self.pDrop = float(pDrop)
		self.pDuplicate = float(pDuplicate)
		self.pError = float(pError)
		self.maxOrder = float(maxOrder)
		self.pOrder = float(pOrder)
		self.pDelay = float(pDelay)
    # drop segment if random number is less than pDrop
	def pDropSeg(self):
		rand = str(random.uniform(0,1))
		if rand < self.pdrop:
			return True
		else:
			return False
    # If the segment is not dropped, with probability pDuplicate, forward the STP segment twice back-to-back to UDP
    def pDupSeg(self):
        print("how to send back to back?")

    # With probability pCorrupt, introduce one bit error (you can simply flip any one bit of data) and forward
    # the STP segment to UDP.
    def pCorrSeg(self, data):
        print("Need to flip one bit of data")

    # save the current STP segment and wait for forwarding of maxOrder segments to UDP before forwarding the saved STP
    # segment to UDP
    def maxOrderSeg(self):
        print("Forward to UDP")

    #  pDelay the segment is to be delayed by anywhere between 0 to MaxDelay milliseconds before forwarding to UDP
    def pDelaySeg(self):
        print("Delay")

    #  If the STP segment is not dropped, duplicated, corrupted, re-ordered or delayed, forward the STP segment to UDP.
    def forwardSTP(self):
        print("Going to UDP!")

def setUp():
    #take arguments from command line
    ip = sys.argv[1]
    port = int(sys.argv[2])
    file_name = sys.argv[3]
    MWS = int(sys.argv[4])
    MSS = int(sys.argv[5])
    gamma = int(sys.argv[6])
    timeout = 500 + 250 * gamma
    pDrop = float(sys.argv[7])
    pDuplicate = float(sys.argv[8])
    pCorrupt = float(sys.argv[9])
    pOrder = float(sys.argv[10])
    maxOrder = float(sys.argv[11])
    pDelay = float(sys.argv[12])
    maxDelay = float(sys.argv[13])
    seed = int(sys.argv[14])

    #set up the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    seq_num = 0
    ack_num = 0
    un_ack = 0
    oldest_un_ack = 0

    state_preconnection = True
    state_syn_sent = False
    state_timeout = False
    state_established = True
    state_end = False

    packet_transmitted = 0
    packet_dropped = 0

    timenow = 0
    timestart = 0

    
