---

# Secure Chat Application

The Secure Chat Application is a simple client-server chat system that provides end-to-end encryption and decryption of messages exchanged between clients and the server. The application uses sockets for communication and implements encryption and decryption using pre-trained deep learning models.

## Features

- **End-to-end Encryption**: All messages sent between clients and the server are encrypted before transmission and decrypted upon receipt, ensuring privacy and security.
  
- **Real-time Communication**: Clients can exchange messages with each other in real-time through the server, enabling instant communication.

- **Simple User Interface**: The client-side interface is designed to be user-friendly, allowing users to send and receive messages easily.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/secure-chat-application.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Server

1. Run the server script:

   ```bash
   python server.py
   ```

2. The server will start listening for incoming client connections on the specified host and port.

### Client

1. Run the client script:

   ```bash
   python client.py
   ```

2. Enter the server's host IP address and port number when prompted.

3. Once connected, you can start sending and receiving messages with other clients connected to the server.

## Dependencies

- Python 3.x
- NumPy
- TensorFlow/Keras (for machine learning models)
- tkinter (for GUI components)

## Contributors

- [Aatish Sharma](https://github.com/Aatish1066)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize the README.md file further based on your project's specific details and requirements!
