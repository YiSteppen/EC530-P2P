from zeroconf import ServiceInfo, Zeroconf, ServiceBrowser, ServiceListener
import socket
import threading
import time

class MyServiceListener(ServiceListener):
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print(f"Discovered service {name} at {socket.inet_ntoa(info.addresses[0])}:{info.port}")
        # Here you could add logic to connect to the discovered service

def register_service(zeroconf, name, port=12345):
    service_type = "_EC530-P2P._tcp.local."
    service_name = f"{name}.{service_type}"
    server_name = f"{socket.gethostname()}.local."
    address = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
    info = ServiceInfo(service_type, service_name, addresses=[address], port=port, server=server_name)
    print(f"Registering service {service_name}, type {service_type}")
    zeroconf.register_service(info)
    return info

def listen_for_connections(port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print("Listening for connections...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode('utf-8')}")
                conn.sendall(data)  # Echo back the received data

def main():
    zeroconf = Zeroconf()
    listener = MyServiceListener()
    browser = ServiceBrowser(zeroconf, "_EC530-P2P._tcp.local.", listener)

    # Register service
    service_name = "Yi_S"
    service_info = register_service(zeroconf, service_name)

    # Start listening thread
    server_thread = threading.Thread(target=listen_for_connections)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            # Main loop can handle user input or other tasks
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Unregistering service and shutting down.")
    finally:
        zeroconf.unregister_service(service_info)
        zeroconf.close()

if __name__ == "__main__":
    main()