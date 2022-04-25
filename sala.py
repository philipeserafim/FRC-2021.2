import os
import random
import threading
from client import Client
from server import Server

class SalaBatePapo:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.rooms_list = []
  
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
    # Criar um servidor
    server = Server(titulo, self.host, self.port, max_clients)

    # Colocar servidor na lista
    self.rooms_list.append(server)
    thread = threading.Thread(target = server.run)
    thread.start()

    server_host, server_port = server.get_network()
    client = Client(server_host, server_port)
    client.run()
    return
  
  def joinRoom(self):
    resp_host = input("Digite o ip do host: ")
    resp_port = int(input("Digite a porta: "))

    client = Client(resp_host, resp_port)
    client.run()  
  
  def leftRoom(self):
    # Deixar um servidor
    ...

port = random.randint(0, 9999)

sala = SalaBatePapo('127.0.0.1', port)
sala.run()
