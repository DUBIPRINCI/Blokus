import socket
import threading
from Blokus import Blokus

HOST = "0.0.0.0"
PORT = 50000

parties = {}  # {party_name: {"game": Blokus, "clients": [client_sockets], "num_players": int, "started": False}}
players = {}

def handle_client(client_socket, client_address):
    try:
        pseudo = client_socket.recv(1024).decode("utf-8").strip()
        if not pseudo:
            print(f"Client {client_address} a envoyé un pseudo invalide.")
            client_socket.close()
            return

        print(f"Pseudo reçu de {client_address}: {pseudo}")
        players[client_socket] = pseudo
        client_socket.sendall(f"Bienvenue sur le serveur, {pseudo}.\n".encode("utf-8"))

        while True:
            data = client_socket.recv(1024).decode("utf-8").strip()
            if not data:
                print(f"Client {pseudo} ({client_address}) déconnecté.")
                break

            print(f"Commande reçue de {pseudo} ({client_address}): {data}")
            parts = data.split(" ", 1)
            command = parts[0]

            if command == "/create":
                party_name, num_players = parts[1].split()
                create_party(client_socket, party_name, int(num_players))
            elif command == "/join":
                party_name = parts[1]
                join_party(client_socket, party_name)
            elif command == "/start":
                start_party(client_socket)
            elif command == "/quit":
                client_socket.sendall("Déconnexion...\n".encode("utf-8"))
                break
            else:
                client_socket.sendall(f"Commande inconnue : {command}\n".encode("utf-8"))

    except ConnectionResetError:
        print(f"Connexion réinitialisée par {client_address}.")
    except Exception as e:
        print(f"Erreur avec {client_address}: {e}")
    finally:
        disconnect_client(client_socket)

def create_party(client_socket, party_name, num_players):
    if party_name in parties:
        client_socket.sendall("Une partie avec ce nom existe déjà.\n".encode("utf-8"))
        return

    parties[party_name] = {
        "game": Blokus(num_players),
        "clients": [client_socket],
        "num_players": num_players,
        "started": False,
    }
    client_socket.sendall(f"Partie '{party_name}' créée avec succès.\n".encode("utf-8"))

def join_party(client_socket, party_name):
    if party_name not in parties:
        client_socket.sendall("Cette partie n'existe pas.\n".encode("utf-8"))
        return

    party = parties[party_name]
    if len(party["clients"]) >= party["num_players"]:
        client_socket.sendall("La partie est pleine.\n".encode("utf-8"))
        return

    party["clients"].append(client_socket)
    client_socket.sendall(f"Vous avez rejoint la partie '{party_name}'.\n".encode("utf-8"))

def start_party(client_socket):
    for party_name, party in parties.items():
        if client_socket in party["clients"]:
            if len(party["clients"]) == party["num_players"]:
                party["started"] = True
                broadcast(party, "La partie a commencé !")
                return
            else:
                client_socket.sendall("Tous les joueurs ne sont pas encore connectés.\n".encode("utf-8"))
                return

    client_socket.sendall("Vous n'êtes pas dans une partie.\n".encode("utf-8"))

def broadcast(party, message):
    for client in party["clients"]:
        client.sendall(f"{message}\n".encode("utf-8"))

def disconnect_client(client_socket):
    pseudo = players.pop(client_socket, None)
    for party_name, details in parties.items():
        if client_socket in details["clients"]:
            details["clients"].remove(client_socket)
            print(f"Client {pseudo} déconnecté de la partie {party_name}")
            break

    client_socket.close()
    print(f"Connexion avec {pseudo or 'un client inconnu'} fermée.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Serveur en cours d'exécution...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connecté : {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()