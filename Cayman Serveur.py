import socket
import win32com.client

# Définition du port d'écoute
SERVER_PORT = 61000

# Fonction pour obtenir l'état réel de la machine
def get_machine_state():
    cayman_server = win32com.client.Dispatch("Cayman.Wirelist")
    machine_info = cayman_server.GetInterface("ICaymanMachineInfo")
    return machine_info.sProdGetProdState()

# Fonction pour traiter la connexion d'un client
def handle_client(client_socket):
    # Réception du message du client
    message = client_socket.recv(1024).decode("utf-8")
    print(f"Message reçu du client : {message}")

    # Envoi de l'état réel de la machine au client
    machine_state = get_machine_state()
    client_socket.sendall(str(machine_state).encode("utf-8"))

    # Fermeture de la connexion client
    client_socket.close()

# Fonction pour démarrer le serveur
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", SERVER_PORT))
        server_socket.listen()
        print(f"Serveur en écoute sur le port {SERVER_PORT}")

        # Boucle de traitement des clients
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connecté depuis {client_address}")
            handle_client(client_socket)

# Démarrage du serveur
start_server()
