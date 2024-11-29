import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 50000

parties = {}  # Dictionnaire pour gérer les parties
clients = {}  # {client_socket: (pseudo, party_name)}


def broadcast(message, party_name=None, exclude=None):
    """Envoyer un message à tous les clients d'une partie donnée."""
    if party_name and party_name in parties:
        for client in parties[party_name]['clients']:
            if client != exclude:  # Exclure un client spécifique si nécessaire
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    pass


def handle_client(client_socket, client_address):

    """Gérer un client connecté."""
    try:
        # Recevoir le pseudo
        client_name = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = (client_name, None)
        print(f"[CONNEXION] {client_address[0]} s'est connecté en tant que '{client_name}'")

        # client_socket.sendall("Bienvenue sur le serveur Blokus !".encode('utf-8'))

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("CREATE"):
                _, party_name, num_players = data.split()
                if party_name not in parties:
                    parties[party_name] = {
                        'num_players': int(num_players),
                        'clients': [client_socket],
                        'started': False  # Indique si la partie a démarré
                    }
                    clients[client_socket] = (client_name, party_name)
                    client_socket.sendall(f"Partie '{party_name}' créée. En attente d'autres joueurs.".encode('utf-8'))
                else:
                    client_socket.sendall(f"Erreur : Une partie avec le nom '{party_name}' existe déjà.".encode('utf-8'))

            elif data.startswith("JOIN"):
                _, party_name = data.split()
                if party_name in parties and not parties[party_name]['started']:
                    if len(parties[party_name]['clients']) < parties[party_name]['num_players']:
                        parties[party_name]['clients'].append(client_socket)
                        clients[client_socket] = (client_name, party_name)
                        broadcast(f"{client_name} a rejoint la partie '{party_name}'.", party_name)
                        if len(parties[party_name]['clients']) == parties[party_name]['num_players']:
                            broadcast(f"La partie '{party_name}' est prête. Tapez '/start' pour commencer.", party_name)
                    else:
                        client_socket.sendall(f"Erreur : La partie '{party_name}' est pleine.".encode('utf-8'))
                else:
                    client_socket.sendall(f"Erreur : La partie '{party_name}' n'existe pas ou a déjà démarré.".encode('utf-8'))

            elif data.startswith("MESSAGE"):
                _, message = data.split(" ", 1)
                client_name, party_name = clients[client_socket]
                if party_name and not parties[party_name]['started']:
                    timestamp = datetime.now().strftime("%H:%M")
                    broadcast(f"{client_name} [{timestamp}] : {message}", party_name)

            elif data.startswith("START"):
                _, party_name = data.split()
                if party_name in parties:
                    if len(parties[party_name]['clients']) == parties[party_name]['num_players']:
                        parties[party_name]['started'] = True
                        broadcast("/start", party_name)  # Signal de démarrage
                        print(f"La partie '{party_name}' a démarré.")
                    else:
                        client_socket.sendall("Erreur : Tous les joueurs ne sont pas connectés.".encode('utf-8'))

            elif data == "LIST":
                available_parties = "\n".join([
                    f"{index + 1}. {name} ({len(info['clients'])}/{info['num_players']} joueurs)"
                    for index, (name, info) in enumerate(parties.items())
                    if not info['started']  # Exclut les parties démarrées
                ])
                if available_parties:
                    print(f"Parties trouvées :\n{available_parties}")
                    client_socket.sendall(f"Parties disponibles :\n{available_parties}".encode('utf-8'))
                else:
                    print("Aucune partie disponible pour LIST.")
                    client_socket.sendall("Aucune partie disponible pour le moment.".encode('utf-8'))

            elif data == "QUIT" or data == "EXIT":
                break

    except:
        pass
    finally:
        disconnect_client(client_socket)


def disconnect_client(client_socket):
    """Gérer la déconnexion d'un client."""
    if client_socket in clients:
        client_name, party_name = clients[client_socket]
        print(f"[DÉCONNEXION] {client_name} ({client_socket.getpeername()[0]}) s'est déconnecté.")
        if party_name and party_name in parties:
            parties[party_name]['clients'].remove(client_socket)
            if not parties[party_name]['clients']:
                del parties[party_name]  # Supprimer la partie si plus de joueurs
            else:
                broadcast(f"{client_name} a quitté la partie '{party_name}'.", party_name)
        del clients[client_socket]
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Serveur Blokus en cours d'exécution...")
    
    # Démarrer un thread pour gérer les commandes du terminal
    threading.Thread(target=handle_server_commands, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

def handle_server_commands():
    """Gérer les commandes saisies dans le terminal du serveur."""
    while True:
        command = input()
        if command == "/party_list":
            print("Liste des parties :")
            if parties:
                for name, info in parties.items():
                    print(f"- {name}: {len(info['clients'])}/{info['num_players']} joueurs (Démarrée : {info['started']})")
            else:
                print("Aucune partie en cours.")
        else:
            print("Commande inconnue. Commandes disponibles : /party_list")

if __name__ == "__main__":
    start_server()