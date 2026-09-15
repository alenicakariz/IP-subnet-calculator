def ask_try():                                                      #for retrying inputs
    ans = input("\nTry Again? (y/n): ").strip().lower()
    if ans != "y":
        print("\nThank you. Goodbye!")
        exit()
    return True

while True:
    #1 -- user input and validation
    ip = input("Enter IP/CIDR: ")

    if "/" not in ip:
        print("Invalid format. Use IP/CIDR, e.g. 192.168.1.1/24")
        ask_try()
        continue

    ip = ip.split("/")
    ip_string = ip[0]
    subnet_mask = ip[1]

    if not subnet_mask.isdigit():
        print("Invalid subnet mask. It must be a number digit.")
        ask_try()
        continue

    subnet_mask = int(subnet_mask)

    if not (subnet_mask <= 32 and subnet_mask >= 0):
        print("Invalid subnet mask. It must be between 0 - 32.")
        ask_try()
        continue

    ip_string = ip_string.split(".")

    if len(ip_string) != 4:
        print("Invalid IP length. There must be 4 octets.")
        ask_try()
        continue

    is_valid = True
        
    for a in ip_string:
        if not a.isdigit():
            print("Invalid IP address. It must be a number.")
            is_valid = False

    for a in ip_string:
        if int(a) > 255 or int(a) < 0:
            print("Invalid IP address. It must not exceed 255 or be negative.")
            is_valid = False

    if is_valid == False:
            ask_try()
            continue

    print("\nIP & SUBNET DETAILS")
    print(f"IP Address: \t\t{".".join(ip_string)}")
    print(f"Subnet Prefix: \t\t/{subnet_mask}")

    #2 -- octet to binary
    ip_binary = ""
    def octet_to_binary(octet):                                 #function for decimal to binary
        return format(int(octet), "08b")                        #padding is 0, min width is 8, b is binary
        
    for octet in ip_string:                                     #loops through all ip string (decimal)
        ip_binary += octet_to_binary(octet)                     #combines all octets to form a 32-bit binary string

    # print(f"IP address (binary): {ip_binary}")

    #3 -- show subnet mask from prefix
    def binary_to_octet(binary):                                #function for binary to decimal
        octets = []
        for i in range(0,32,8):                                 #starts at 0, stops at 31, increments by 8
            octets.append(binary[i:i+8])                        #becomes a list of four 8-character binary strings  
        return ".".join(str(int(octet,2)) for octet in octets)  #parses binary into decimal and combines it with dots

    mask_binary = "1" * subnet_mask + "0" * (32 - subnet_mask)  #generates 32 bits total
    subnet_mask_dotted = binary_to_octet(mask_binary)           #binary to decimal of subnet mask

    print(f"Subnet Mask: \t\t{subnet_mask_dotted}")
    # print(f"Subnet Mask (binary):  {mask_binary}")

    #4 -- calculate network address
    network_binary = ""
    for bit in range(32):                                       #starts at 0, stops at 31
        if int(ip_binary[bit]) * int(mask_binary[bit]) == 1:    #performs bitwise gets network binary address from ip and subnet mask
            network_binary += "1"                               #adds one if part of network
        else:
            network_binary += "0"                               #adds zero if not

    network_address = binary_to_octet(network_binary)           #binary to decimal of network address
    print(f"Network Address: \t{network_address}")
    # print(f"Network Address (binary):  {network_binary}")

    #5 -- calculate broadcast address
    broadcast_binary = ""                                       #placeholder for broadcast address in binary

    for bit in range(32):                           
        if bit < subnet_mask:                                   #checks how many bits within subnet mask
            broadcast_binary += network_binary[bit]             #copies the network bits from the network address
        else:   
            broadcast_binary += "1"                             #sets all host bits to 1 for the broadcast address

    broadcast_address = binary_to_octet(broadcast_binary)       #binary to decimal of broadcast address
    print(f"Broadcast Address: \t{broadcast_address}")
    # print(f"Broadcast Address (binary): {broadcast_binary}")

    #6 -- usable hosts: first and last
    host_bits = 32-subnet_mask                                  #host bits
    total_hosts = 2**host_bits                                  #total hosts = 2^n
    usable_hosts = total_hosts-2                                #total usable hosts 2^n-2

    first_host = int(network_binary, 2)+1                       #first usable host is +1 the network address
    last_host = int(broadcast_binary, 2)-1                      #last usable host is -1 the broadcast address
                                                                #int(<binary_string>, 2) converts a binary string to a decimal integer

    first_usable_host = binary_to_octet(format(first_host, "032b"))     #padding is 0, min width is 32, b is binary
    last_usable_host = binary_to_octet(format(last_host, "032b"))       #format(<integer>, "032b") converts decimal integer to 32-bit string 
                                                                        #... then convert this binary string to decimal IPv4
    print(f"Usable hosts: \t\t{usable_hosts} hosts")
    print(f"First usable hosts: \t{first_usable_host}")
    print(f"Last usable hosts: \t{last_usable_host}")

    ask_try()
    