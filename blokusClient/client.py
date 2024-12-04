import asyncio
import os

HOST = '127.0.0.1'
PORT = 50000


async def receive_messages(reader, game_started):
    """Recevoir et afficher des messages du serveur."""
    while True:
        try:
            message = await reader.read(4096)
            if not message:
                break
            decoded_message = message.decode('utf-8').strip()  # Supprime les espaces ou sauts de ligne inutiles

            # Si la partie commence, on bloque les entrées utilisateur
            if decoded_message == "/start":
                cls()
                print("Début de la partie")
                game_started.set_result(True)  # Signal que le jeu a démarré
                break

            # Afficher le message reçu
            print("\r\033[K" + decoded_message)  # Efface la ligne actuelle avant d'afficher le message
            print("> ", end="", flush=True)  # Réaffiche le prompt proprement après le message
        except Exception as e:
            print(f"Erreur lors de la réception de messages : {e}")
            break


async def send_messages(writer, party_name, game_started):
    """Envoyer des messages au serveur depuis le lobby."""
    while not game_started.done():  # Boucle tant que la partie n'a pas démarré
        try:
            print("> ", end="", flush=True)  # Affiche le prompt pour la saisie
            message = await asyncio.to_thread(input)
            print("\033[F\033[K", end="")  # Efface la ligne entière (prompt + texte saisi)

            if message.lower() == "/exit":
                writer.write("EXIT\n".encode('utf-8'))  # Envoyer une commande explicite au serveur
                await writer.drain()
                print("Vous quittez le lobby...")
                break
            elif message.lower() == "/start":
                writer.write(f"START {party_name}\n".encode('utf-8'))
                await writer.drain()
            else:
                writer.write(f"MESSAGE {message}\n".encode('utf-8'))
                await writer.drain()
        except Exception as e:
            print(f"Erreur lors de l'envoi de messages : {e}")
            break


async def lobby(reader, writer, party_name):
    """Gérer le lobby d'une partie."""
    print(f"Vous êtes maintenant dans le lobby de la partie '{party_name}'.")
    print("Tapez '/exit' pour quitter le lobby.")
    print("Tapez '/start' pour lancer la partie (si tout le monde est connecté).")
    print("Envoyez un message pour communiquer avec les autres joueurs.")

    game_started = asyncio.Future()  # Future pour suivre si le jeu a démarré

    await asyncio.gather(
        receive_messages(reader, game_started),
        send_messages(writer, party_name, game_started)
    )


async def main():
    pseudo = input("Entrez votre nom de joueur : ")

    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(pseudo.encode('utf-8'))
    await writer.drain()

    print("Bienvenue sur le serveur Blokus !")

    while True:
        print("\n====== MENU ======")
        print("1. Créer une partie")
        print("2. Rejoindre une partie")
        print("3. Quitter")
        print("==================")

        choice = input("Choisissez une option : ")
        if choice == "1":
            party_name = input("Nom de la partie : ")
            num_players = input("Nombre de joueurs (2-4) : ")
            writer.write(f"CREATE {party_name} {num_players}\n".encode('utf-8'))
            await writer.drain()
            await lobby(reader, writer, party_name)

        elif choice == "2":
            writer.write("LIST".encode('utf-8'))
            await writer.drain()
            print("Veuillez patienter pour voir la liste des parties...")

            # Lire la réponse du serveur
            data = await reader.read(4096)  # Lire la liste des parties disponibles
            decoded_data = data.decode('utf-8').strip()  # Supprime les espaces inutiles

            if decoded_data.startswith("Parties disponibles"):
                print(decoded_data)
                
                # Demander à l'utilisateur de choisir une partie par son numéro
                while True:
                    try:
                        selection = int(input("Entrez le numéro de la partie à rejoindre : "))
                        lines = decoded_data.split("\n")[1:]  # Liste des parties
                        if 1 <= selection <= len(lines):
                            party_name = lines[selection - 1].split(".")[1].strip().split(" ")[0]  # Extraire le nom
                            writer.write(f"JOIN {party_name}\n".encode('utf-8'))
                            await writer.drain()
                            
                            # Lire la réponse du serveur pour confirmer ou refuser l'accès
                            response = await reader.read(1024)
                            decoded_response = response.decode('utf-8').strip()
                            if decoded_response.startswith("Erreur"):
                                print(decoded_response)  # Affiche le message d'erreur du serveur
                            else:
                                print(decoded_response)
                                await lobby(reader, writer, party_name)
                            break
                        else:
                            print("Numéro invalide. Réessayez.")
                    except ValueError:
                        print("Veuillez entrer un numéro valide.")
            else:
                print("Aucune partie disponible pour le moment.")

        elif choice == "3":
            writer.write("QUIT\n".encode('utf-8'))
            await writer.drain()
            print("Déconnexion...")
            break

        else:
            print("Option invalide. Réessayez.")

    writer.close()
    await writer.wait_closed()

def cls():
    """Nettoyer le terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    asyncio.run(main())