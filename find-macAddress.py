#parallel_query using threads.py
import base64
import getpass
import re
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
startTime = datetime.now()
threads = []

# Function to get user Password (Note: not a secure way but useful)
def getpassword():
    password = getpass.getpass("Enter your password: ")
    return password

#Function to implement multi threads to login into devices simultaously : saving time
def checkparallel(ip,usr,passwd,macaddress):
    device = ConnectHandler(device_type='cisco_ios', ip=ip, username=usr, password=passwd)
    #device.send_command("enable", "neteng")
    host = device.send_command("show version | inc switch")
    macoutput = device.send_command("show mac address-table | inc "+macaddress)
    #print(macaddress)
    #print(macoutput)
    if len(macoutput)==0:
        print("MAC not Found")
        exit()
    pattern = re.compile(r'Fa\d+/\d+|Gi\d+/\d+')

        # Define the regular expression pattern

        # Find all matches in the file content
    matches = pattern.findall(macoutput)
    port = matches[0]
        # Print the matches
        #for match in matches:
    #print(port)
    portoutput=device.send_command("sh  int "+port +" switchport | inc Mode")
    pattern = r'Administrative Mode:\s+(trunk|static access)'
    match = re.search(pattern, portoutput)
   # print(match)
    string1=match.group().split(":")[1]
    word = string1[1:]
    if(word=='trunk'):
        pass
    else:
        print("-"*20)
        print(host.split()[0])
        print(port)
        int_description=device.send_command("sh  int "+port +" description")
        slot1 = int_description.split()[-1]
        slot2 = int_description.split()[-2]
        if 'up' in slot2:
            print(slot1)
        else:
            print("User: ",slot2, slot1)
        #print(macaddress)
        print("-"*20)
        exit()



    #manually add switch ip's to the list
#devices=["10.103.16.11"]
# get user Details

#call the function to store the password.



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

macaddress=""
result =[]
usr="scripty"
def decryptcredential(pwd):
    rvalue=base64.b64decode(pwd)
    rvalue=rvalue.decode()
    return rvalue
mypwd=b'bmV0ZW5n'
passwd = decryptcredential(mypwd)
pyeng = '''
┏┓   ┏┓   
┃┃┓┏ ┣┏┓┏┓
┣┛┗┫━┗┛┗┗┫
   ┛     ┛
 '''

print(pyeng)
inp=input("Do you know mac-address?Y:N  :")
if inp=="Y":
    macaddress=input("Enter mac id: ")
else:
    ip=input("Enter Ip address: ")
    check_mac(ip)
    macaddress=result[0]
    print()
    print("-"*20)
    print("MAC found:"+macaddress)


devices = ["10.103.16.11","10.103.16.12","10.103.16.13","10.103.16.14","10.103.16.17", "10.103.16.21", "10.103.16.26"]
for n in devices:
    ip=n
    t = Thread(target=checkparallel, args= (ip,usr,passwd,macaddress))
    t.start()
    threads.append(t)
#wait for all threads to completed
for t in threads:
    t.join()
print ("\nTotal script execution time in Seconds:")
print(datetime.now() - startTime)


