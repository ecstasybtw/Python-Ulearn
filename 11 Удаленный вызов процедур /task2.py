import socket
import json
import pandas as pd

def get_website(df, name):
    value = df[df['Name'] == name]['Website'].values[0]
    return value

def get_country(df, name):
    value = df[df['Name'] == name]['Country'].values[0]
    return value

def get_number_of_employees(df, name):
    value = df[df['Name'] == name]['Number of employees'].values[0]
    return str(value)

def get_description(df, name):
    value = df[df['Name'] == name]['Description'].values[0]
    return value

def start_server():
    df = pd.read_csv("organizations.csv")

    host = "127.0.0.32"
    port = 12345

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    client, addr = server_socket.accept()

    while True:
        data = client.recv(1024).decode()
        request = json.loads(data)
        operation = request['operation']
        name = request['name']

        to_response = None
        if operation == 'get_website':
            to_response = get_website(df, name)
        elif operation == 'get_country':
            to_response = get_country(df, name)
        elif operation == 'get_number_of_employees':
            to_response = get_number_of_employees(df, name)
        elif operation == 'get_description':
            to_response = get_description(df, name)

        response = json.dumps({'result': to_response})
        client.sendall(response.encode())
