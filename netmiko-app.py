from netmiko import ConnectHandler
import json

line = "-"*100

def config_control_vlan_S1(s1):
    '''config vlan 101 to host'''
    commands = [
        "vlan 101",
        "name control-data",
        "exit",
        "int gi0/1",
        "switchport access vlan 101",
        "int gi1/0",
        "switchport access vlan 101",
        "do wr"
    ]
    net_connect = ConnectHandler(**s1)
    result = net_connect.send_config_set(commands)
    net_connect.disconnect()
    return result

def config_ospf(router:dict,pid:str , vrf:str, networks:list, default:bool=False):
    '''config ospf on a specific vrf on a router'''
    commands = [
        f"router ospf {pid} vrf {vrf}"
    ]
    commands += [f"network {network} {wild} area {area}" for network, wild, area in networks]
    if default:
        commands.append("default-information originate")
    commands.append("do wr")

    net_connect = ConnectHandler(**router)
    result = net_connect.send_config_set(commands)
    net_connect.disconnect()
    return result

def config_pat(router:dict, inside:list,  interface:str, inside_interfaces:list):
    '''config PAT on a router'''
    commands = [
        "no ip access-list standard PAT-INSIDE",
        "ip access-list standard PAT-INSIDE"
    ]
    commands += [f"permit {ip}" for ip in inside]
    commands += [
        "exit",
        f"ip nat inside source list PAT-INSIDE interface {interface} vrf control-data overload",
        f"int {interface}",
        "ip nat outside"
    ]
    for interface in inside_interfaces:
        commands += [f"int {interface}", "ip nat inside"]
    commands.append("do wr")

    net_connect = ConnectHandler(**router)
    result = net_connect.send_config_set(commands)
    net_connect.disconnect()
    return result

def deny_ssh_telnet(router:dict):
    '''deny ssh and telnet on a specific vrf on a router'''
    commands = [
        "no ip access-list standard DENY-SSH-TELNET",
        "no ip access-list extended DENY-SSH-TELNET",
        "ip access-list standard DENY-SSH-TELNET",
        "permit 192.168.118.0 0.0.0.255",
        "permit 10.30.6.0 0.0.0.255",
        "permit 172.31.146.0 0.0.0.15",
        "deny any log",
        "exit",
        "line vty 0 4",
        f"access-class DENY-SSH-TELNET in vrf-also",
        "do wr"
    ]
    net_connect = ConnectHandler(**router)
    result = net_connect.send_config_set(commands)
    net_connect.disconnect()
    return result

def main():
    '''main'''
    with open("./hosts.json", "r", encoding="utf-8") as file:
        hosts = json.load(file)

    # Config VLAN 101 S1
    print("Configuring VLAN 101 on S1")
    result = config_control_vlan_S1(hosts["S1"])
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    # Config OSPF R1
    networks_r1 = [
        ("192.168.1.0", "0.0.0.255", "0"),
        ("192.168.2.0", "0.0.0.255", "0")
    ]
    print("Configuring OSPF on R1")
    result = config_ospf(hosts["R1"], "2", "control-data", networks_r1)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    # Config OSPF R2
    networks_r2 = [
        ("192.168.2.0", "0.0.0.255", "0"),
        ("192.168.3.0", "0.0.0.255", "0")
    ]
    print("Configuring OSPF on R2")
    result = config_ospf(hosts["R2"], "2", "control-data", networks_r2, True)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    # Config PAT R2
    inside_ips = [
        "192.168.1.0 0.0.0.255",
        "192.168.2.0 0.0.0.255",
        "192.168.3.0 0.0.0.255"
    ]
    inside_interfaces = [
        "gi0/1",
        "gi0/2",
    ]
    print("Configuring PAT on R2")
    result = config_pat(hosts["R2"], inside_ips, "gi0/3", inside_interfaces)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    # Deny SSH and Telnet on R1
    print("Denying SSH and Telnet on R1")
    result = deny_ssh_telnet(hosts["R1"])
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    # Deny SSH and Telnet on R2
    print("Denying SSH and Telnet on R2")
    result = deny_ssh_telnet(hosts["R2"])
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

if __name__ == "__main__":
    main()
