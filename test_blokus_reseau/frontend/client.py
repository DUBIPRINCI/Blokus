import os
import asyncio
import sys

HOST = "127.0.0.1"
PORT = 50000

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    pseudo = input("Choisissez un pseudo (4 à 20 caractères) : ").strip()
    
    if 3 < len(pseudo) < 21:
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            writer.write(pseudo.encode("utf-8"))
            await writer.drain()
            
            response = await reader.read(1024)
            print(response.decode("utf-8"))

            await menu(reader, writer)

        except ConnectionRefusedError:
            print("Impossible de se connecter au serveur.")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
        finally:
            print("Fermeture du client.")
            writer.close()
            await writer.wait_closed()
    else:
        print("Le pseudo doit contenir entre 4 et 20 caractères.")

async def menu(reader, writer):
    while True:
        cls()
        print("======================")
        print("1. Créer une partie")
        print("2. Rejoindre une partie")
        print("3. Quitter")
        print("======================")
        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            party_name = input("Nom de la partie : ").strip()
            num_players = input("Nombre de joueurs : ").strip()
            writer.write(f"/create {party_name} {num_players}".encode("utf-8"))
            await writer.drain()
            response = await reader.read(1024)
            print(response.decode("utf-8"))
            input("Appuyez sur Entrée pour continuer...")
        elif choix == "2":
            party_name = input("Nom de la partie : ").strip()
            writer.write(f"/join {party_name}".encode("utf-8"))
            await writer.drain()
            response = await reader.read(1024)
            print(response.decode("utf-8"))
            input("Appuyez sur Entrée pour continuer...")
        elif choix == "3":
            writer.write("/quit".encode("utf-8"))
            await writer.drain()
            break
        else:
            print("Option invalide, veuillez réessayer.")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    asyncio.run(main())