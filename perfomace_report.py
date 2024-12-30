import netmiko
import getpass


# Function to get user Password (Note: not a secure way but useful)
def getpassword():
    password = getpass.getpass("Enter your Scripty password: ")
    return password

# Device details
device_ip = '10.103.16.12'
username = 'scripty'
password = getpassword()


# Netmiko device connection
device = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'password': password
}

# Connect to device
net_connect = netmiko.ConnectHandler(**device)

# CPU usage
cpu_output = net_connect.send_command('show processes cpu')
print("CPU Usage:")
print(cpu_output)

# Memory usage
memory_output = net_connect.send_command('show memory')
print("\nMemory Usage:")
print(memory_output)

# Bandwidth usage (interface-specific)
interface = 'GigabitEthernet0/1'
bandwidth_output = net_connect.send_command(f'show interface {interface} statistics')
print(f"\nBandwidth Usage on {interface}:")
print(bandwidth_output)

# Close connection
net_connect.disconnect()
