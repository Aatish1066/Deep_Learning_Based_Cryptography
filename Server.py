import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.running = True

        self.start_server()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")
        self.accept_clients()

    def accept_clients(self):
        while self.running:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.client_sockets.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                # print(f"Received message: {message}")
                self.broadcast(message, client_socket)
            except Exception as e:
                print(f"Error: {e}")
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.client_sockets:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
                    self.client_sockets.remove(client_socket)

    def close(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()
        self.running = False

def main():
    host = '127.0.0.1'  # Localhost
    port = 5555
    server = Server(host, port)

if __name__ == "__main__":
    main()
