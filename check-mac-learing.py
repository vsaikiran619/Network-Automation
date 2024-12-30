import getpass
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
threads = []
def getpassword():
    password = getpass.getpass("Enter your password: ")
    return password

usr = input("enter username:")
passwd = getpassword()
ip = input("Enter Ip address:")
result =[]
def checkparallel1(result,dev,usr,passwd):
    device = ConnectHandler(device_type='brocade_fastiron', ip=dev, username=usr, password=passwd)
    device.enable()
    #device.send_command("enable", "neteng")
    mac = device.send_command("show arp | inc "+ip)
    if len(mac)==0:
        device.disconnect()
        pass
    else:
        realmac = mac.split()
        result.append(realmac[2])
    device.disconnect()


def check_mac(ip):
    devices = ["10.103.155.1","10.103.155.2"]
    for n in devices:
        dev=n
        t = Thread(target=checkparallel1, args= (result,dev,usr,passwd))
        t.start()
        threads.append(t)
    #wait for all threads to completed
    for t in threads:
        t.join()

check_mac(ip)
print(result[0])

