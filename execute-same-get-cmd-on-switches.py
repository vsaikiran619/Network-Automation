import getpass
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread

def configure_switch(ip, username, password):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
    }
    
    net_connect = ConnectHandler(**device)
    
    commands = input("Eter show command to run on all switches: ")
   # print(commands) 
    output = net_connect.send_command(commands)
    print('*' * 50)
    print(f"Output from {ip}:")
    print('*' * 50)
    print(output)

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    switches = ["10.103.16.11"]
    
    threads = []
    for ip in switches:
        t = Thread(target=configure_switch, args=(ip, username, password))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    print("All switches Queried")

