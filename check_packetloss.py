import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(host, count=4):
    """
    Ping a host and return the packet loss percentage.
    
    :param host: The host to ping (IP address or domain name).
    :param count: Number of ping requests to send.
    :return: Packet loss percentage or None if an error occurs.
    """
    try:
        # Run the ping command
        output = subprocess.run(
            ["ping", "-c", str(count), host],
            capture_output=True,
            text=True
        ).stdout
        
        # Extract the packet loss percentage using regex
        packet_loss_match = re.search(r'(\d+)% packet loss', output)
        if packet_loss_match:
            packet_loss = int(packet_loss_match.group(1))
            return packet_loss
        else:
            raise ValueError("Could not parse packet loss from ping output.")
    
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None

def check_packet_loss(ip_dict, max_workers=10):
    """
    Check packet loss for each IP in the dictionary and update the values.
    
    :param ip_dict: Dictionary with hostnames as keys and IP addresses as values.
    :param max_workers: Maximum number of threads to use.
    :return: Updated dictionary with packet loss percentages as values.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_host, ip): host for host, ip in ip_dict.items()}
        for future in as_completed(future_to_ip):
            host = future_to_ip[future]
            try:
                results[host] = future.result()
            except Exception as e:
                print(f"Error processing {host}: {e}")
                results[host] = None
    return results

# Example usage
ip_dict = {
    "VGS_prod": "10.180.16.131",
    "DCA_prod": "10.170.16.131",
    "BNA_Prod": "10.160.16.16",
}

packet_loss_results = check_packet_loss(ip_dict)
for host, loss in packet_loss_results.items():
    print(f"Host: {host}, Packet loss: {loss}%")

