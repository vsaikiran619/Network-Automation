from pysnmp.hlapi import *

def get_snmp_data(host, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            return float(varBind[1])

def main():
    host = '10.103.16.12'  # Replace with your switch IP address
    community = 'net2555'  # Replace with your community string

    # OIDs for CPU and memory usage (Replace with appropriate OIDs for your switch)
    cpu_oid = '1.3.6.1.4.1.9.2.1.57.0'  # Example OID for Cisco CPU usage
    mem_used_oid = '1.3.6.1.4.1.9.2.1.8.0'  # Example OID for Cisco used memory
    mem_free_oid = '1.3.6.1.4.1.9.2.1.9.0'  # Example OID for Cisco free memory

    cpu_usage = get_snmp_data(host, community, cpu_oid)
    mem_used = get_snmp_data(host, community, mem_used_oid)
    mem_free = get_snmp_data(host, community, mem_free_oid)

    if cpu_usage is not None:
        print(f"CPU Usage: {cpu_usage}%")

    if mem_used is not None and mem_free is not None:
        mem_total = mem_used + mem_free
        mem_usage_percentage = (mem_used / mem_total) * 100
        print(f"Memory Usage: {mem_usage_percentage:.2f}%")

if __name__ == "__main__":
    main()

