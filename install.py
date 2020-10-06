import os

print(u"""

\u001b[32;1mdb   d8b   db d888888b d8888b. d88888b d88888b  .d88b.  db    db
88   I8I   88   `88'   88  `8D 88'     88'     .8P  Y8. `8b  d8'
88   I8I   88    88    88oobY' 88ooooo 88ooo   88    88  `8bd8'
Y8   I8I   88    88    88`8b   88~~~~~ 88~~~   88    88  .dPYb.
`8b d8'8b d8'   .88.   88 `88. 88.     88      `8b  d8' .8P  Y8.
 `8b8' `8d8'  Y888888P 88   YD Y88888P YP       `Y88P'  YP    YP

\u001b[4m  01010111 01101001 01110010 01100101 01000110 01101111 01111000  """)
print("\n                   install 1.2.0\n")

os.system("xterm -e sudo apt update")
os.system("xterm -e pip3 install scapy")
os.system("xterm -e pip3 install netfilterqueue")


print("installed...:)")
