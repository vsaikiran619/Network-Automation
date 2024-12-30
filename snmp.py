from pysnmp.hlapi import *

def collect_interface_descriptions(ip, community):
    # OID for interface descriptions in Cisco devices
    oid = '1.3.6.1.2.1.2.2.1.2'  # ifDescr

    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),  # Use SNMPv2c (mpModel=1)
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    )

    descriptions = []

    for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
        if errorIndication:
            print(f"SNMP Error: {errorIndication}")
            return None
        elif errorStatus:
            print(f"SNMP Error: {errorStatus}")
            return None
        else:
            for varBind in varBinds:
                descriptions.append(varBind[1].prettyPrint())

    return descriptions

# Example usage
if __name__ == "__main__":
    ip = '10.103.16.11'   # Replace with your Cisco switch IP address
    community = 'net2555'  # Replace with your SNMP community string

    interface_descriptions = collect_interface_descriptions(ip, community)
    if interface_descriptions:
        print("Interface Descriptions:")
        for description in interface_descriptions:
            print(description)
    else:
        print("Failed to retrieve interface descriptions")

