import socket

def scan_ports(ip:str, ports:list) -> dict:
    scan_info = {}

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((ip, port))
            sock.close()

            if result == 0:
                scan_info[port] = True
            else:
                scan_info[port] = False
        except Exception as e:
            print(f"Error: {e}")
            scan_info[port] = "Error"
    return scan_info

def scan_targets(targets: dict, ports: list) -> dict:
    for target_names in targets:
        port_status = scan_ports(targets[target_names], ports)
        targets[target_names] = {"IP" : targets[target_names]}
        for port in port_status:
            targets[target_names][port] = port_status[port]
    return targets
