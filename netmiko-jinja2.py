from pathlib import Path
import json

from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

line = "-" * 100

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)


def render_template(template_name: str, **context) -> str:
    """Render a Jinja2 template into a Cisco IOS command list."""
    template = env.get_template(template_name)
    return template.render(**context)


def send_commands(device: dict, commands: str) -> str:
    """Send a rendered configuration block to a device."""
    net_connect = ConnectHandler(**device)
    try:
        result = net_connect.send_config_set(commands.splitlines())
    finally:
        net_connect.disconnect()
    return result


def config_control_vlan_S1(s1: dict) -> str:
    """Configure VLAN 101 on S1."""
    commands = render_template("control_vlan.j2")
    return send_commands(s1, commands)


def config_ospf(router: dict, pid: str, vrf: str, networks: list, default: bool = False) -> str:
    """Configure OSPF on a specific VRF on a router."""
    commands = render_template(
        "ospf.j2",
        pid=pid,
        vrf=vrf,
        networks=networks,
        default=default,
    )
    return send_commands(router, commands)


def config_pat(router: dict, inside: list, interface: str, inside_interfaces: list) -> str:
    """Configure PAT on a router."""
    commands = render_template(
        "pat.j2",
        inside_networks=inside,
        outside_interface=interface,
        inside_interfaces=inside_interfaces,
    )
    return send_commands(router, commands)


def deny_ssh_telnet(router: dict) -> str:
    """Deny SSH and Telnet on a specific VRF on a router."""
    commands = render_template(
        "deny_ssh_telnet.j2",
        permit_rules=[
            {"network": "192.168.118.0", "wildcard": "0.0.0.255"},
            {"network": "10.30.6.0", "wildcard": "0.0.0.255"},
            {"network": "172.31.146.0", "wildcard": "0.0.0.15"},
        ],
    )
    return send_commands(router, commands)


def main() -> None:
    """Main entry point."""
    with open("./hosts.json", "r", encoding="utf-8") as file:
        hosts = json.load(file)

    print("Configuring VLAN 101 on S1")
    result = config_control_vlan_S1(hosts["S1"])
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    networks_r1 = [
        ("192.168.1.0", "0.0.0.255", "0"),
        ("192.168.2.0", "0.0.0.255", "0"),
    ]
    print("Configuring OSPF on R1")
    result = config_ospf(hosts["R1"], "2", "control-data", networks_r1)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    networks_r2 = [
        ("192.168.2.0", "0.0.0.255", "0"),
        ("192.168.3.0", "0.0.0.255", "0"),
    ]
    print("Configuring OSPF on R2")
    result = config_ospf(hosts["R2"], "2", "control-data", networks_r2, True)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    inside_ips = [
        "192.168.1.0 0.0.0.255",
        "192.168.2.0 0.0.0.255",
        "192.168.3.0 0.0.0.255",
    ]
    inside_interfaces = ["gi0/1", "gi0/2"]
    print("Configuring PAT on R2")
    result = config_pat(hosts["R2"], inside_ips, "gi0/3", inside_interfaces)
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    print("Denying SSH and Telnet on R1")
    result = deny_ssh_telnet(hosts["R1"])
    print("Configuration Finished, Result: ")
    print(line)
    print(result)
    print(line)

    print("Denying SSH and Telnet on R2")
    result = deny_ssh_telnet(hosts["R2"])
    print("Configuration Finished, Result: ")
    print(result)
    print(line)


if __name__ == "__main__":
    main()
