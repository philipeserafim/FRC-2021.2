import os
import socket 
from _thread import *
import threading

from user import User

class Server:
  def __init__(self, name, host, port, max_clients):
    self.name = name
    self.HOST = host
    self.PORT = port
    self.max_clients = max_clients
    self.connected_clients = []

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

  def controla_conexao(self, client):
    message = f"Para entrar no bate papo deve primeiro digitar seu apelido: "

    client.send(message.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')

    # Checar nickname
    has_nickname = self.checar_nickname(nickname)

    while has_nickname:
      client.send(("Já possui um usuário com esse nome. Por favor outro nome: ").encode('utf-8'))
      nickname = client.recv(1024).decode('utf-8')    
      has_nickname = self.checar_nickname(nickname)


    user = User(nickname, client)
    self.connected_clients.append(user)

    message = f"Bem vindo ao bate papo {self.name}! Convide seus amigos, ip: {self.HOST}, porta: {self.PORT}"

    client.send(message.encode('utf-8'))

    self.no_tag_message(f"{user.nickname} entrou na sala!", user)
    self.receber_mensagem(user)

  def no_tag_message(self, message, user):
    for client in self.connected_clients:
      if user.client != client.client:
        try:
          client.client.send(message.encode('utf-8'))
        except:
          continue

  def checar_nickname(self, nickname):
    for user in self.connected_clients:
      if (user.nickname == nickname):
        return True
    
    return False

  def encerra_conexao(self):
    for user in self.connected_clients:
      user.client.close()

    self.socket.close()

  def enviar_mensagem(self, message, sender):
    for user in self.connected_clients:
      if sender.client != user.client:
        try:
          user.client.send(f"<{sender.nickname}>: {message}".encode('utf-8'))
        except:
          continue

  def receber_mensagem(self, user):
    while True:
      try:
        msg = user.client.recv(2048).decode('utf-8')

        if msg == '/exit':
          user.client.close()
          self.connected_clients.remove(user)
          self.no_tag_message(f"{user.nickname} saiu do bate papo!", user)
          return

        self.enviar_mensagem(msg, user)
      except:
        break

# chatRoom = Server('Teste', '127.0.0.1', 5000, 3)
# chatRoom.run()

