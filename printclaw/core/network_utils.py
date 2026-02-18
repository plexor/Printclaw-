import socket


def local_ip_addresses() -> list[str]:
    ips = {"127.0.0.1"}
    try:
        _, _, resolved = socket.gethostbyname_ex(socket.gethostname())
        ips.update(resolved)
    except socket.gaierror:
        pass
    return sorted(ips)
