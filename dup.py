# The provided string
mysrt = '''
Vl16                           up             up
Gi0/1                          up             up       rkolusu_PC
Gi0/2                          up             up       "1st Floor printer"
Gi0/5                          up             up
Gi0/6                          up             up       "1st floor conference room"
Gi0/7                          up             up       kudaya pc
Gi0/8                          up             up       ratnakar_Phone
Gi0/10                         up             up       tpavan PC
Gi0/11                         up             up       jpeter pc
Gi0/13                         up             up       "suresh phone"
Gi0/14                         up             up       "dmounika"
Gi0/16                         up             up       " Tharun_trainee"
Gi0/17                         up             up       "S_savitri_laptop"
Gi0/18                         up             up       "dvadlam-pc"
Gi0/19                         up             up       "ksriram_db"
Gi0/20                         up             up       "sushma_pc"
Gi0/28                         up             up       electrician_1stfloor_PC
Gi0/31                         up             up       Corpsys-Dlink-HUB
Gi0/36                         up             up       lsheguri PC
Gi0/37                         up             up       "vsai PC"
Gi0/38                         up             up       "asuresh PC"
Gi0/39                         up             up       routing_test
Gi0/41                         up             up       "Pavankumar Reddy"
Gi0/44                         up             up       "Maditya-HR"
Gi0/45                         up             up       suresh_pc
Gi0/47                         up             up
Gi0/48                         up             up
'''

# Split the string into lines
lines = mysrt.strip().split('\n')

# Iterate over each line and check if a description is present
for line in lines:
    parts = line.split()
    if len(parts) > 3:
        description = ' '.join(parts[3:])
        #print(f"Interface {parts[0]} has description: {description}")
    else:
        print(f"Interface {parts[0]} has no description")


