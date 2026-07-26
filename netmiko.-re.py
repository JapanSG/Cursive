from netmiko import ConnectHandler
import json
import re

def get_active_interfaces(router:dict):
    '''get active interfaces on a router'''
    net_connect = ConnectHandler(**router)
    output = net_connect.send_command("show ip int brief")
    net_connect.disconnect()
    active_interfaces = []
    for line in output.splitlines():
        if re.search(r"up\s+up", line):
            interface = line.split()[0]
            active_interfaces.append(interface)
    return active_interfaces

def get_interface_uptime(router:dict, interface:str):
    '''get interface uptime on a router'''
    net_connect = ConnectHandler(**router)
    output = net_connect.send_command(f"show int {interface}")
    net_connect.disconnect()
    uptimes = None
    for line in output.splitlines():
        if re.search(r"Last input", line):
            uptimes = [item.strip() for item in line.split(", ")]
            break
    return uptimes

def main():
    '''main'''
    with open("./hosts.json", "r", encoding="utf-8") as file:
        hosts = json.load(file)

    routers_name = ["R1", "R2"]
    line = "-" * 100
    print(line)
    for router_name in routers_name:
        router = hosts[router_name]
        active_interfaces = get_active_interfaces(router)
        print(f"Active interfaces on {router_name}: {active_interfaces}")

        for interface in active_interfaces:
            uptimes = get_interface_uptime(router, interface)
            if uptimes:
                print(f"{interface} on {router_name}: {uptimes[0]}, {uptimes[1]}, {uptimes[2]}")
            else:
                print(f"{interface} on {router_name}: None")
        print(line)

if __name__ == "__main__":
    main()
