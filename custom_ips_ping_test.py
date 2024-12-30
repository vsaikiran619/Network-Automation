import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging

def ping_ip(ip):
    try:
        # Ping the IP address
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.STDOUT, universal_newlines=True)
        return (ip, True, output)
    except subprocess.CalledProcessError as e:
        return (ip, False, e.output)
    except Exception as e:
        return (ip, False, str(e))

def ping_custom_ips(ip_list, max_workers=20):
    reachable_ips = []
    unreachable_ips = []

    # Use ThreadPoolExecutor to ping IP addresses concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                ip_str, is_reachable, output = future.result()
                if is_reachable:
                    logging.info(f'{ip_str} is reachable')
                    reachable_ips.append(ip_str)
                else:
                    logging.warning(f'{ip_str} is not reachable')
                    unreachable_ips.append(ip_str)
            except Exception as e:
                logging.error(f'Error pinging {ip}: {e}')
                unreachable_ips.append(ip)

    return reachable_ips, unreachable_ips

def main():
    parser = argparse.ArgumentParser(description='Ping a list of custom IP addresses.')
    parser.add_argument('ips', metavar='IP', type=str, nargs='+', help='IP addresses to ping')
    parser.add_argument('--workers', type=int, default=20, help='Number of concurrent workers')
    parser.add_argument('--log', type=str, default='ping_log.log', help='Log file name')

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info('Starting to ping IP addresses...')
    reachable, unreachable = ping_custom_ips(args.ips, args.workers)
    
    logging.info(f"Reachable IPs: {reachable}")
    logging.info(f"Unreachable IPs: {unreachable}")
    
    print(f"Reachable IPs: {reachable}")
    print(f"Unreachable IPs: {unreachable}")

if __name__ == '__main__':
    main()

