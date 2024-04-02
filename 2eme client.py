import socket
import time

# Server address and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 61000

def display_machine_state(machine_state):

    """
    Présente l'état de la machine à l'aide d'un dictionnaire de recherche pour une meilleure lisbilité.
    """
    state_descriptions = {
        0: "Offline",
        1: "Connecting",
        2: "Online (waiting)",
        3: "Running Wire List",
        4: "The production waits with a \"message from machine\" dialog.",
        5: "Machine performs load/unload, close/open, cut or feed",
        6: "Machine waits with a “message from machine” dialog during load/unload, close/open, cut or feed",
        10: "A wire was produced complete",
        11: "A batch was produced complete",
        12: "A total was produced complete",
        13: "A list total was produced complete",
        14: "A grand total was produced complete",
        15: "The production was produced complete",
        16: "The production was confirmed",
        20: "Wirelist opening file started",
        21: "Wirelist opening file completed",
        22: "WireList new started",
        23: "WireList new completed",
        24: "WireList save started",
        25: "WireList save completed",
        26: "WireList save as… started",
        27: "WireList save as… completed",
        99: "Cayman is closing"
    }
    print(f"État de la machine : {state_descriptions.get(machine_state, 'Inconnu')}")

def connect_and_monitor():
    """
    Establishes a connection, sends an optional message (can be removed),
    receives data from the server, and displays the machine state with error handling.
    """
    while True:
        try:
            # Établir la connexion au serveur
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
                print(f"Client connecté au serveur {SERVER_ADDRESS}")

                # Optional message to the server
                message = "Initialisation du client"
                client_socket.sendall(message.encode("utf-8"))

                # Recevoir et traiter les données du serveur
                while True:
                    received_data = client_socket.recv(1024).decode("utf-8")
                    if received_data:
                        # Analyser et afficher l'état de la machine
                        try:
                            machine_state = int(received_data)
                            display_machine_state(machine_state)
                        except ValueError:
                            print(f"Erreur: conversion de la réponse du serveur impossible : {received_data}")
                    else:
                        print("Serveur déconnecté. Réinitialisation de la connexion...")
                        break

        except ConnectionRefusedError:
            print("Serveur indisponible. Nouvelle tentative de connexion dans 5 secondes...")
            time.sleep(5)

        except Exception as e:
            print(f"Erreur inattendue : {e}")
            print("Réinitialisation de la connexion dans 5 secondes...")
            time.sleep(5)

# Démarrage de la boucle de surveillance
connect_and_monitor()
