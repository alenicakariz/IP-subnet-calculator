# IP Subnet Calculator

A command-line Python script that calculates subnet details from an IP address and CIDR prefix.

## What it does

Given an IP and CIDR (e.g. `192.168.1.130/26`), it calculates:
- Subnet mask (dotted-decimal)
- Network address
- Broadcast address
- First and last usable host
- Total and usable host counts

All calculations are done manually using binary string conversion and bitwise logic (no external libraries).

Enter an IP address with CIDR notation when prompted:

```
Enter IP/CIDR: 192.168.1.130/26

IP & SUBNET DETAILS
IP Address:             192.168.1.130
Subnet Prefix:          /26
Subnet Mask:            255.255.255.192
Network Address:        192.168.1.128
Broadcast Address:      192.168.1.191
Usable hosts:           62 hosts
First usable hosts:     192.168.1.129
Last usable hosts:      192.168.1.190
```
You'll be asked if you want to calculate another subnet after each run.

## How it works

1. **Input validation** — checks the IP/CIDR format, subnet mask range (0–32), and that each octet is a valid number between 0–255.
2. **IP to binary** — each octet is converted to an 8-bit binary string and combined into a 32-bit string.
3. **Subnet mask from CIDR** — builds a 32-bit mask string (prefix number of `1`s, followed by `0`s).
4. **Network address** — bitwise AND between the IP and mask, bit by bit.
5. **Broadcast address** — keeps the network bits, sets all host bits to `1`.
6. **Host range** — first usable host is network address + 1; last usable host is broadcast address − 1; usable host count is `2^(host bits) - 2`.

## Notes
- Written for learning purposes. It demonstrates binary/decimal conversion and subnetting logic without relying on Python's `ipaddress` module.
