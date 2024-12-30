#parallel_query using threads.py
import getpass
import smtplib
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
def checkparallel(ip,usr,passwd):
    device = ConnectHandler(device_type='cisco_ios', ip=ip, username=usr, password=passwd)
    #device.send_command("enable", "neteng")
    uptime = device.send_command("show ver | inc uptime")
    SerialNumber = device.send_command("sh ver | inc System serial")
    #Version = device.send_command("sh ver | inc software")
    portSecurity = device.send_command("show port-security  address | inc Dynamic")
    intStatus = device.send_command("sh int status | inc notconnect")
    print(portSecurity)
    #print(ip,uptime,SerialNumber,Version,portSecurity,intStatus)
    print('*'*50)
    print(f"{uptime}\n {SerialNumber}")
   # if len(portSecurity)<1:
    #    print("NONE")
    #else:
     #   print(f"The following ports are not configured Port-security but a device is connected.\n",portSecurity)
    print(f"\nThe followin ports are not connected and not inuse.\n",intStatus)
    print('*'*50)
    print("\n")

    #manually add switch ip's to the list
devices = ["10.103.16.11","10.103.16.13","10.103.16.14","10.103.16.17", "10.103.16.21", "10.103.16.26"]


# get user Details
usr=input("Enter your Username:")

#call the function to store the password.
passwd=getpassword()


for n in devices:
    ip=n
    t = Thread(target=checkparallel, args= (ip,usr,passwd))
    t.start()
    threads.append(t)
#wait for all threads to completed
for t in threads:
    t.join()
print ("\nTotal script execution time in Seconds:")
print(datetime.now() - startTime)





