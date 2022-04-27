import os
import random
import threading
from client import Client
from room import Room
from server import Server

class Application:
  def __init__(self, host, port):
    self.host = host
    self.port = port
  
  def run(self):
    while True:
      print("1 - Criar uma sala")
      print("2 - Entrar em uma sala existente")
      print("0 - Sair do programa")

      resp = int(input("Selecione uma opção: "))

      if resp == 0:
        os._exit(0)

      if resp == 1:
        titulo = input("Escreva o nome da sua sala de bate papo: ")
        max_clients = int(input("Qual vai ser o limite máximo de participantes? "))
        self.createRoom(titulo, max_clients)
         
      if resp == 2:
        self.joinRoom()

  def createRoom(self, titulo, max_clients):
    # Criar uma sala
    room = Room(titulo, self.host, self.port, max_clients)

    # Roda a sala em uma outra thread
    thread = threading.Thread(target = room.run)
    thread.start()

    # Conectando com a sala
    self.connectToRoom(self.host, self.port)
    

  def connectToRoom(host, port):
    # Conecta a sala
    client = Client(host, port)
    client.run()

  
  def joinRoom(self):
    resp_host = input("Digite o ip do host: ")
    resp_port = int(input("Digite a porta: "))

    client = Client(resp_host, resp_port)
    client.run()  
  
  def leftRoom(self):
    # Deixar um servidor
    ...

port = random.randint(0, 9999)

server = Server('127.0.0.1', 5000)
app = Application('127.0.0.1', port)

app.run()
