#Gizem Kendüzler - 27400502538
#Gökalp Eren Kangal - 14048889428
#Ecem Alakuş - 10049980898


import socket
import random
import pandas as pd

# Read the Excel file containing the list of plate codes for all cities
plate_data = pd.read_excel('plate_list.xlsx')

# Set up TCP socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
clientNumber = 1

while True:

    print(f"Waiting for {clientNumber}th client connection")
    print("Server is waiting for connection...")

    connection, client_address = server_socket.accept()
    print("Client connected from:",client_address)
    # Randomly choose a city and its plate code
    random_city_index = random.randint(0, len(plate_data) - 1)
    random_city = plate_data.loc[random_city_index, 'CityName']
    correct_plate_code = plate_data.loc[random_city_index, 'PlateNumber']
    
    clientNumber += 1

    try:
        while True:
            # Send the city name to the client
            connection.sendall(random_city.encode())

            # Receive prediction from client
            prediction = connection.recv(1024).decode()
            print(f"Received from client: {prediction}")

            if prediction == "END":
                connection.close()
                server_socket.close()
                exit()

            # Check if the prediction is numeric
            if not prediction.isdigit():
                connection.sendall("You have entered a non-numeric value. Please enter a valid plate code.".encode())
                continue

            prediction = int(prediction)
            if prediction == correct_plate_code:
                connection.sendall("Correct!".encode())
            elif prediction < 1 or prediction > 81:
                connection.sendall("Number exceeds the range. Please enter a valid plate code.".encode())
            else:
                guessed_city = plate_data.loc[plate_data['PlateNumber'] == prediction, 'CityName'].iloc[0]
                connection.sendall(f"You have entered the plate code of {guessed_city}!".encode())

    except ConnectionResetError:
        print("")
    finally:
        connection.close()  # Close the connection with the current client

server_socket.close()  # Close the server socket when the game ends