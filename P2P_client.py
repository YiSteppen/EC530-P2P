import socket

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        response = s.recv(1024)
        print(f"Received reply: {response.decode('utf-8')}")

if __name__ == "__main__":
    host = input("Enter the host IP address:")  # The IP address of the server
    port = 12345  # The port number should match the server
    message = "Hello from the client!"
    send_message(host, port, message)