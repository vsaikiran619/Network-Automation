import re
import ipaddress
from ipwhois import IPWhois
import pexpect
import smtplib
import io
import sys
import getpass
from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
#import datetime

# Get today's date
today = datetime.now()

# Extract the month from today's date and get the month name
current_month_name = today.strftime("%B")

# Print the current month name
#print(f"Current month: {current_month_name}")

# Function to get user Password (Note: not a secure way but useful)
def getpassword():
    password = getpass.getpass("Enter your password: ")
    return password


def capture_print_statements(user,passwd,asa_mgmt_ip, ip_address, cidr, subnet_mask, location_info):

    # Create a StringIO object to capture output
    output_capture = io.StringIO()

    # Redirect standard output to the StringIO object
    sys.stdout = output_capture

    
    

   # Block Ip on ASA 
    def login_to_asa(user,passwd,ip, subnet, subnet_mask,location_info, prompt='#'):
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("[Pp]assword")
            ssh.sendline(passwd)
            enable_status = ssh.expect([">", "#"])
            if enable_status == 0:
                ssh.sendline("enable")
                ssh.expect("[Pp]assword")
                ssh.sendline(passwd)
                ssh.expect(prompt)
                ssh.sendline("conf t")
            acl_commands = [
                f'object-group network BLOCKED-NW',
                f'network-object {subnet} {subnet_mask}',]
            full_output = ''
            for command in acl_commands:
                ssh.sendline(command)
                ssh.expect(prompt)
                #full_output += f"{ssh.before}\n{ssh.after}\n"
            ssh.sendline("end")
            #verification_command = 'sh run | inc 113.161.61.0'
            #ssh.sendline(verification_command)
            #ssh.expect(prompt)
            # Capture the verification command and its output
            #full_output += f"{ssh.before}\n{ssh.after}\n"
            #print(full_output)

            #print("Full Command Output:\n", full_output)
            print(f"Blocked: {subnet}, {subnet_mask}")
            print("Origin:",location_info)
           


    
    
    #calling blocking function on ASA:
    login_to_asa(user, passwd, asa_mgmt_ip, cidr,subnet_mask, location_info)


    
    
    
    startTime = datetime.now()
    
    
    
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
    to_address = 'net-routing-hyd@corp.untd.com'
    subject = 'PyEng - Blocking ASA Auth Failures '
    body = captured_output
    msg = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("10.103.32.62", 25)
        server.sendmail(from_address, to_address, msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":

    pyeng = '''
┏┓   ┏┓
┃┃┓┏ ┣┏┓┏┓
┣┛┗┫━┗┛┗┗┫
   ┛     ┛
 '''
    print(pyeng)
    # Get user details
    user = 'scripty'
    passwd = getpassword()
    asa_mgmt_ip = '10.103.16.200'
    # Ask user for IP address
    ip_address = input("Enter IP address to Block: ")

    def get_ip_subnet(ip):
        try:
            # Perform the WHOIS lookup
            obj = IPWhois(ip)
            results = obj.lookup_rdap(depth=1)
            result = obj.lookup_rdap()
            remarks = result['network']['remarks'] if 'network' in result and 'remarks' in result['network'] else []
            location_info = remarks[0]['description'] if remarks and 'description' in remarks[0] else 'N/A' 
            #city = result['network']['city'] if 'network' in result and 'city' in result['network'] else 'N/A'
            #state = result['network']['state'] if 'network' in result and 'state' in result['network'] else 'N/A'
            #country = result['network']['country'] if 'network' in result and 'country' in result['network'] else 'N/A'
    
            
            cidr = results.get('network', {}).get('cidr', None)
            if cidr is None:
                return 'Subnet not found'
            return cidr,location_info
        except Exception as e:
            return f"Error occurred: {str(e)}"
    
    def cidr_to_subnet_mask(cidr):
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            return str(network.netmask)
        except ValueError as e:
            return f"Invalid CIDR notation: {str(e)}"
    
    def is_valid_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    # Validate the IP address
    if is_valid_ip(ip_address):
        cidr,location_info = get_ip_subnet(ip_address)
        print(location_info)
        print(f"CIDR for IP {ip_address}: {cidr}")
        subnet_mask = cidr_to_subnet_mask(cidr)
        ip_base = cidr.split('/')[0]   
        print(f"Subnet Mask for {cidr}: {subnet_mask}")
    else:
        print("Invalid IP address. Please enter a valid IP address.")
    print(subnet_mask)
    print(ip_base)
    #calling this =>function which inturn call all other functions within the code:
    #captured_output = capture_print_statements(user, passwd, asa_mgmt_ip, ip_base, subnet_mask)
    
        # calling this function which in turn calls all other functions within the code:
    captured_output = capture_print_statements(user, passwd, asa_mgmt_ip, ipaddress, ip_base, subnet_mask, location_info)
    print("Captured Output:")
    print(captured_output)
#   calling mail function to return output to mail
    send_mail(captured_output)

