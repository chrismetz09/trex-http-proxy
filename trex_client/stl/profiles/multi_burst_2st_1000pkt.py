from trex_stl_lib.api import *

# 1 clients MAC override the LSB of destination
class STLS1(object):

    def __init__ (self):
        self.fsize  =64; # the size of the packet 
        self.burst_size = 2


    def create_stream (self):

        # create a base packet and pad it to size
        size = self.fsize - 4; # no FCS
        base_pkt =  Ether()/IP(src="16.0.0.1",dst="48.0.0.1")/UDP(dport=12,sport=1025)
        base_pkt1 =  Ether()/IP(src="16.0.0.2",dst="48.0.0.1")/UDP(dport=12,sport=1025)
        pad = max(0, size - len(base_pkt)) * 'x'


        return STLProfile( [ STLStream( isg = 10.0, # star in delay 
                                        name    ='S0',
                                        packet = STLPktBuilder(pkt = base_pkt/pad),
                                        mode = STLTXSingleBurst( pps = 10, total_pkts = self.burst_size),
                                        next = 'S1'), # point to next stream 

                             STLStream( self_start = False, # stream is  disabled enable trow S0
                                        name    ='S1',
                                        packet  = STLPktBuilder(pkt = base_pkt1/pad),
                                        mode    = STLTXMultiBurst( pps = 1000,pkts_per_burst = 4,ibg = 1000000.0,count = 5)
                                        )

                            ]).get_streams()


    def get_streams (self, direction = 0, **kwargs):
        # create 1 stream 
        return self.create_stream() 


# dynamic load - used for trex console or simulator
def register():
    return STLS1()




