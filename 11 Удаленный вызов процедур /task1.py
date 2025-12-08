import socket
import pandas as pd


def get_site_and_county(df, name):
    subset = df[df['Name'] == name]
    if not subset.empty:
        website = subset['Website'].iloc[0]
        country = subset['Country'].iloc[0]
        return f"Сайт: {website}. Страна: {country}"
    return None


def start_server():
    df = pd.read_csv('organizations.csv')
    host = "127.0.0.32"
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    client, addr = server.accept()

    while True:
        name = client.recv(1024)

        if not name:
            break

        name = name.decode().strip()

        if name == 'exit':
            break
        else:
            response = get_site_and_county(df, name)
            client.send(response.encode())

    client.close()
    server.close()
