import subprocess
import time
import logging

# Configure logging
logging.basicConfig(filename='ping_monitor.log', level=logging.INFO, format='%(asctime)s %(message)s')

def ping(host):
    """Ping a host and return True if the host is reachable, else False."""
    try:
        output = subprocess.check_output(['ping', '-c', '1', host], stderr=subprocess.STDOUT, universal_newlines=True)
        if "1 received" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def monitor_tunnel(remote_ip, interval=60):
    """Monitor the IPsec tunnel by pinging the remote endpoint."""
    while True:
        if ping(remote_ip):
            logging.info(f'Tunnel to {remote_ip} is up.')
        else:
            logging.warning(f'Tunnel to {remote_ip} is down.')
        
        # Wait for the specified interval before the next ping
        time.sleep(interval)

if __name__ == "__main__":
    # Replace with the IP address of the remote endpoint of the IPsec tunnel
    remote_ip = '10.180.16.16'
    
    # Ping interval in seconds
    interval = 60
    
    monitor_tunnel(remote_ip, interval)

