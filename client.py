import socket

def udp_client():
    # Ask user for the client port number
    client_port = int(input("Enter the port number for the client: "))

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('localhost', client_port))  # Bind to localhost and the user-defined port

    while True:
        # Get message from user
        message = input("Enter a message to send to the server: ")
        # Send the message to the server
        client_socket.sendto(message.encode('utf-8'), ('localhost', 5000))

        # Receive response from server
        response, _ = client_socket.recvfrom(1024)
        response = response.decode('utf-8')
        print("Received from server:", response)

        # If certain response is received, close the socket
        if response == "Port is not allowed to communicate":
            print("Closing the client socket.")
            client_socket.close()
            break

if __name__ == '__main__':
    udp_client()
