switchname = input("Enter Switch name:=> eg. switch1-1: ")

# Define the dictionary with the switch IP address
switch_dict = {
    'switch1-1': '10.103.16.11',
    'switch1-2': '10.103.16.12',
    'switch1-3': '10.103.16.13',
    'switch6a-4': '10.103.16.17',
    'switch6a-5': '10.103.16.21',
    'switch6a-6': '10.103.16.26',
    'switch6a-1': '10.103.16.13',
}

# Assign the value of the switch key to the variable X
try:
    X = switch_dict[switchname]

    print(X)
except:
    print("Switch not found :(")





def LoginToSwitch(Switchname,usr,passwd):

  #  portSecurity = check_PortSecurity():
   #     pass
    pass
