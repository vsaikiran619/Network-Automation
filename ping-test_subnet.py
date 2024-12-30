import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_ip(ip):
    try:
        # Ping the IP address
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', str(ip)], stderr=subprocess.STDOUT)
        return (str(ip), True)
    except subprocess.CalledProcessError:
        return (str(ip), False)

def ping_subnet(subnet, max_workers=20):
    net = ipaddress.ip_network(subnet)
    reachable_ips = []
    unreachable_ips = []

    # Use ThreadPoolExecutor to ping IP addresses concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in net.hosts()}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                ip_str, is_reachable = future.result()
                if is_reachable:
                   # print(f'{ip_str} is reachable')
                    reachable_ips.append(ip_str)
                else:
                    #print(f'{ip_str} is not reachable')
                    unreachable_ips.append(ip_str)
            except Exception as e:
                print(f'Error pinging {ip}: {e}')
                unreachable_ips.append(str(ip))

    return reachable_ips, unreachable_ips

# Example usage
subnet = '10.181.44.0/24'  # Replace with your desired subnet
reachable, unreachable = ping_subnet(subnet)
print('='*30)
print(f"Reachable IPs: {reachable}")
print('='*30)
print("\n\n\n\n")
print(f"Unreachable IPs: {unreachable}")

