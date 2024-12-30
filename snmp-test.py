from pysnmp.hlapi import *

def collect_snmp_data(ip, community, oid):
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False
    )

    for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
        if errorIndication:
            print(f"SNMP Error: {errorIndication}")
            return None
        elif errorStatus:
            print(f"SNMP Error: {errorStatus}")
            return None
        else:
            for varBind in varBinds:
                return varBind.prettyPrint()

# Example usage
if __name__ == "__main__":
    ip = '192.168.1.1'
    community = 'public'
    oid = '1.3.6.1.2.1.1.5.0'  # Example OID for system name

    value = collect_snmp_data(ip, community, oid)
    if value:
        print(f"SNMP data retrieved successfully: {value}")
    else:
        print("Failed to retrieve SNMP data")

