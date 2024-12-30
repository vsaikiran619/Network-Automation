from ipwhois import IPWhois
import ipaddress

def get_ip_subnet(ip):
    try:
        # Perform the WHOIS lookup
        obj = IPWhois(ip)
        results = obj.lookup_rdap(depth=1)
        
        # Extract the subnet information
        cidr = results.get('network', {}).get('cidr', None)
        if cidr is None:
            return 'Subnet not found'
        return cidr
    except Exception as e:
        return f"Error occurred: {str(e)}"

def cidr_to_subnet_mask(cidr):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return str(network.netmask)
    except ValueError as e:
        return f"Invalid CIDR notation: {str(e)}"

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Ask user for IP address
ip_address = input("Enter an IP address: ")

# Validate the IP address
if is_valid_ip(ip_address):
    cidr = get_ip_subnet(ip_address)
    print(f"CIDR for IP {ip_address}: {cidr}")

    if '/' in cidr:
        subnet_mask = cidr_to_subnet_mask(cidr)
        print(f"Subnet Mask for {cidr}: {subnet_mask}")
    else:
        print(f"Could not find CIDR notation for IP {ip_address}")
else:
    print("Invalid IP address. Please enter a valid IP address.")

