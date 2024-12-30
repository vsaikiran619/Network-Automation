from pysnmp.hlapi import *
import time

def collect_snmp_data(ip, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    error_indication, error_status, error_index, var_binds = next(iterator)

    if error_indication:
        print(f"Error: {error_indication}")
        return None
    elif error_status:
        print(f"Error: {error_status.prettyPrint()} at {error_index and var_binds[int(error_index) - 1] or '?'}")
        return None
    else:
        for var_bind in var_binds:
            return var_bind.prettyPrint().split('=')[1].strip()

def print_metrics(metrics):
    print("\nNetwork Metrics:")
    for metric_name, value in metrics.items():
        print(f"{metric_name}: {value}")

# Define the SNMP OIDs for the metrics you want to collect
oids = {
    'sysName': '1.3.6.1.2.1.1.5.0',  # System Name
    'sysDescr': '1.3.6.1.2.1.1.1.0',  # System Description
    'ifInOctets': '1.3.6.1.2.1.2.2.1.10.1',  # Inbound Octets on Interface 1
    'ifOutOctets': '1.3.6.1.2.1.2.2.1.16.1',  # Outbound Octets on Interface 1
    'ifInErrors': '1.3.6.1.2.1.2.2.1.14.1',  # Inbound Errors on Interface 1
    'ifOutErrors': '1.3.6.1.2.1.2.2.1.20.1',  # Outbound Errors on Interface 1
    'ifOperStatus': '1.3.6.1.2.1.2.2.1.8.1'  # Operational Status of Interface 1
}

# Example usage
ip = '192.168.1.1'
community = 'public'

while True:
    metrics = {}
    for metric_name, oid in oids.items():
        value = collect_snmp_data(ip, community, oid)
        if value:
            metrics[metric_name] = value
    
    print_metrics(metrics)
    time.sleep(60)  # Collect data every minute
