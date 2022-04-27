import os
import socket 
from _thread import *
import threading

from user import User

class Server:
  def __init__(self, host, port):
    self.HOST = host
    self.PORT = port
    self.rooms_list = []

  def get_network(self):
    return (self.HOST,self.PORT)

  def run(self):
    try: 
      self.cria_conexao_TCP()
      self.aceita_conexao_clients()
    except:
      print("Ocorreu um erro")
      os._exit(1)


  def cria_conexao_TCP(self):
    server = (self.HOST, self.PORT)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      self.socket.bind(server)
    except:
      print("Bind falhou")
      os._exit(1)
    self.socket.listen(self.max_clients)

  
  def aceita_conexao_clients(self):
    while True:
      client, client_address = self.socket.accept()
      thread = threading.Thread(target = self.controla_conexao, args = (client, ))
      thread.start()
  
  def checar_comando(self, client):
    # Pega o comando recebido da Room

    command = client.recv(1024).decode('utf-8')

    if command == '/exit':
      print('Sair do servidor')

    if command == '/add_room':
      print('Adicionar room na lista de rooms')

    if command == 'close_room':
      print('Remover room na lista de rooms')


  def controla_conexao(self, client):
    # Controla a conexão da Room com o Server

    self.checar_comando(client)

  def fechar_servidor(self):
    self.socket.close()


