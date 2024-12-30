import smtplib
import io
import sys
import getpass
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread

    # Function to get user Password (Note: not a secure way but useful)
def getpassword():
    password = getpass.getpass("Enter your password: ")
    return password


def capture_print_statements(usr, passwd):
    # Create a StringIO object to capture output
    output_capture = io.StringIO()

    # Redirect standard output to the StringIO object
    sys.stdout = output_capture


    # Function to implement multi threads to login into devices simultaneously: saving time
    def checkparallel(ip, usr, passwd):
        try:
            device = ConnectHandler(device_type='cisco_ios', ip=ip, username=usr, password=passwd)
            uptime = device.send_command("show ver | inc uptime")
            SerialNumber = device.send_command("sh ver | inc System serial")
            portSecurity = device.send_command("show port-security address | inc SecureDynamic")
            intStatus = device.send_command("sh int status | inc notconnect")

            print(f"{'*' * 50}\nDevice IP: {ip}\n{'*' * 50}")
            print(f"Uptime:\n{uptime}")
            print(f"Serial Number:\n{SerialNumber}")
            print("Port-Security Status:\n")
            if portSecurity:
                print(portSecurity)
            else:
                print("No Port-Security issues detected.")
            print("\nInterface Status:\n")
            if intStatus:
                print(intStatus)
            else:
                print("All interfaces are connected.")
            print(f"{'*' * 50}\n")
        except Exception as e:
            print(f"Failed to connect to {ip}: {e}")

    # Manually add switch IPs to the list
    devices = ["10.103.16.11", "10.103.16.13", "10.103.16.14", "10.103.16.17", "10.103.16.21", "10.103.16.26"]


    threads = []
    startTime = datetime.now()
    
    for ip in devices:
        t = Thread(target=checkparallel, args=(ip, usr, passwd))
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("\nTotal script execution time in seconds:")
    print(datetime.now() - startTime)

    # Reset standard output to its original value
    sys.stdout = sys.__stdout__

    # Get the contents of the StringIO object
    captured_output = output_capture.getvalue()

    # Close the StringIO object
    output_capture.close()

    return captured_output

def send_mail(captured_output):
    from_address = 'bskiran@corp.untd.com'
    to_address = 'bskiran@corp.untd.com'
    subject = 'Test Script'
    body = captured_output
    msg = f"<html><body><pre>{body}</pre></body></html>"

    try:
        server = smtplib.SMTP("10.103.32.62", 25)
        server.sendmail(from_address, to_address, msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":

    usr = input("Enter your Username: ")
    passwd = getpassword()


    captured_output = capture_print_statements(usr, passwd)

    print("Captured Output:")
    print(captured_output)

    send_mail(captured_output)

