from scapy.all import *
from multiprocessing import Process
import random
import os
import time
import sys

devices = []


def startsniff(iface):
    print(u"\u001b[32;1m~CH~   *~*~*~BSSID~*~*~*       ~*~*~ESSID~*~*~    *~DBM~*\u001b[33;1m")
    def changechannel():
        try:
            while True:
                channel = random.randrange(1,14)
                os.system("iw dev {0} set channel {1}".format(iface, channel))
                time.sleep(0.4)
        except KeyboardInterrupt:
            print("\nTHE END!\n")
            sys.exit()

    def packhandler(pack):
        if pack.haslayer(Dot11Beacon):
            essid = pack.getlayer(Dot11Elt)
            essid2 = essid.info

            bssid = pack.getlayer(Dot11)
            bssid2 = bssid.addr3

            channel = str(ord(pack[Dot11Elt:3].info))

            if len(channel) == 1:
                channel = "0" + channel

            dbm = pack.dBm_AntSignal

            if not bssid2 in devices and bssid2 != None:
                devices.append(bssid2)
                space = " " * (18-len(essid2.decode()))
                if essid2.decode() == "":
                    print(" " + str(channel) + "    " + bssid2 + "\t  " + "{hidden}" + "          " + str(dbm))
                else:
                    print(" " + str(channel) + "    " + bssid2 + "\t  " + essid2.decode() + space + str(dbm))

    p = Process(target = changechannel)
    p.start()

    sniff(iface=iface, prn=packhandler)

try:
    startsniff(sys.argv[1])
except KeyboardInterrupt:
    print("THE END!")
    sys.exit()
