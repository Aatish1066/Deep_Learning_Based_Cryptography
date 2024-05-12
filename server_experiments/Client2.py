import socket
import sys
import threading
import numpy as np
import encryption_decryption_functions
import os
import time
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

        # Connect to the server
        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to server.")

    def send_message(self, message):
        try:
            with open(os.devnull, 'w') as fnull:
                sys.stdout = fnull
                encrypted_message = encryption_decryption_functions.encrypt_message(message, np.array([[0, 0, 0, 0, 0, 0, 0, 0]]))
                sys.stdout = sys.__stdout__  # Restore standard output
            self.client_socket.send(encrypted_message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    # def receive_messages(self):
    #     buffer = ""
    #     start_time = time.time()
    #
    #     while self.running:
    #         try:
    #             message = self.client_socket.recv(1024).decode()
    #             if message and not message.startswith("1/1 ["):
    #                 # Append the received message to the buffer
    #                 buffer += message
    #
    #                 # Check if 15 seconds have elapsed since the last message
    #                 if time.time() - start_time >= 15:
    #                     # Suppress progress messages during decryption
    #                     with open(os.devnull, 'w') as fnull:
    #                         sys.stdout = fnull
    #                         decrypted_message = encryption_decryption_functions.decrypt_message(buffer, np.array([[0,0,0,0,0,0,0,0]]))
    #                         sys.stdout = sys.__stdout__  # Restore standard output
    #                     print(f"client name >>{decrypted_message}")
    #
    #                     # Reset buffer and start time for the next 15-second window
    #                     buffer = ""
    #                     start_time = time.time()
    #
    #         except Exception as e:
    #             print(f"Error receiving message: {e}")
    #             break
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                if message and not message.startswith("1/1 ["):
                    # Suppress progress messages during prediction
                    with open(os.devnull, 'w') as fnull:
                        sys.stdout = fnull
                        decrypted_message = encryption_decryption_functions.decrypt_message(message, np.array(
                            [[0, 0, 0, 0, 0, 0, 0, 0]]))
                        sys.stdout = sys.__stdout__  # Restore standard output
                    print(f"client name >>{decrypted_message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    def close(self):
        self.client_socket.close()
        self.running = False

class ClientConsole:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = Client(host, port)
        self.receive_thread = threading.Thread(target=self.client.receive_messages)
        self.receive_thread.start()
        self.send_messages()

    def send_messages(self):
        while self.client.running:
            message = input("Enter message: ")
            self.client.send_message(message)

def main():
    host = '127.0.0.1'  # Localhost
    port = 5555
    ClientConsole(host, port)

if __name__ == "__main__":
    main()
