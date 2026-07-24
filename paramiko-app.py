import paramiko
import json

def main():
    '''main'''
    with open("./hosts.json", "r", encoding="utf-8") as file:
        hosts = json.load(file)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()

    username = "admin"
    key_filename = "./admin.ppk"

    for host in hosts:
        print(f"Connecting to {host}...")
        client.connect(hosts[host], username=username, key_filename=key_filename)
        print("Connected Established")

        # # Get running config and save to ./running-configs/
        stdin, stdout, stderr = client.exec_command('sh run')
        output = stdout.read().decode("utf-8")
        with open(f"running-configs/{host}.txt", "w", encoding="utf-8") as config_file:
            config_file.write(output)
            print(f"Save running config to ./running-configs/{host}.txt")
        print("Closing Connection...")
        client.close()
        print("Connection Closed")

if __name__ == "__main__":
    main()
