from netmiko import ConnectHandler
import json

with open("./hosts.json", "r", encoding="utf-8") as file:
    hosts = json.load(file)

net_connect = ConnectHandler(**hosts["R0"])

output = net_connect.send_command('show ip int brief')
print(output)



