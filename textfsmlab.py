from netmiko import ConnectHandler
import json

LINE = "-"*50

def auto_gen_des(host):
    '''return int description from using sh cdp neighbor'''
    descriptions = {}
    net_connect = ConnectHandler(**host)
    output = net_connect.send_command("sh cdp neigh", use_textfsm=True)
    for line in output:
        local_int = line["local_interface"]
        descriptions[local_int[0:2] + local_int[local_int.find(" ")+1:]] = f"Connect to {line["platform"][0:-1]}{line["neighbor_interface"]} of {line["neighbor_name"][0:line["neighbor_name"].find(".")]}"
    return descriptions

def config_interface_description_R1():
    '''config interface description of a R1'''
    with open("hosts.json", "r",encoding="utf-8") as file:
        hosts = json.load(file)

    host = hosts["R1"]

    # auto generate
    descriptions = auto_gen_des(host)
    descriptions["Gi0/1"] = "Connect to PC"
    commands = []
    for key, item in descriptions.items():
        commands.append(f"int {key}")
        commands.append(f"description {item}")
    net_connect = ConnectHandler(**host)
    output = net_connect.send_config_set(commands)
    print(LINE)
    print(output)
    print(LINE)

    return get_interfaces_description("R1")
    

def config_interface_description_R2():
    '''config interface description of a R2'''
    with open("hosts.json", "r",encoding="utf-8") as file:
        hosts = json.load(file)

    host = hosts["R2"]

    # auto generate
    descriptions = auto_gen_des(host)
    descriptions["Gi0/3"] = "Connect to WAN"
    commands = []
    for key, item in descriptions.items():
        commands.append(f"int {key}")
        commands.append(f"description {item}")
    net_connect = ConnectHandler(**host)
    output = net_connect.send_config_set(commands)
    print(LINE)
    print(output)
    print(LINE)

    return get_interfaces_description("R2")

def config_interface_description_S1():
    '''config interface description of a S1'''
    with open("hosts.json", "r",encoding="utf-8") as file:
        hosts = json.load(file)

    host = hosts["S1"]

    # auto generate
    descriptions = auto_gen_des(host)
    descriptions["Gi1/0"] = "Connect to PC"
    commands = []
    for key, item in descriptions.items():
        commands.append(f"int {key}")
        commands.append(f"description {item}")
    net_connect = ConnectHandler(**host)
    output = net_connect.send_config_set(commands)
    print(LINE)
    print(output)
    print(LINE)

    return get_interfaces_description("S1")

def get_interfaces_description(host):
    '''return interfaces description of a device'''
    with open("hosts.json", "r",encoding="utf-8") as file:
        hosts = json.load(file)

    net_connect = ConnectHandler(**hosts[host])

    if host == "S1":
        valid_int = ["Gi0/1", "Gi1/0"]
    else :
        # Find all interface in control-data vrf
        valid_int = []
        output = net_connect.send_command("sh vrf", use_textfsm=True)
        for line in output:
            if line["name"] == "control-data":
                valid_int += line["interfaces"]

    # Find all up interface
    output = net_connect.send_command("sh ip int br", use_textfsm=True)
    up_int = []
    for line in output:
        if line["status"] == "up" and line["proto"] == "up":
            inte = line["interface"]
            up_int.append(f"{inte[0:2]}{inte[-3:]}")

    print(valid_int)
    print(up_int)
    valid_int = [inte for inte in valid_int if inte in up_int]

    output = net_connect.send_command("sh int des", use_textfsm=True)
    return {line["port"] : line["description"] for line in output if line["port"] in valid_int}

if __name__ == "__main__":
    # print(get_interfaces_description("S1"))
    # config_interface_description_R1()
    pass
