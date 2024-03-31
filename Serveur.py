import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 61000))
s.listen(5)
while True:
    Clientsocket, adress = s.accept()
    print(f" Connection avec {adress} est reussie ")
    Clientsocket.send(bytes("Bienvenue au serveur", "utf-8"))
    Clientsocket.close()