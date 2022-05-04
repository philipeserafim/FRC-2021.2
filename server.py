from http import client
import os
import socket 
import threading
import time
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
      self.aceita_conexao_rooms()
    except:
      print("Ocorreu um erro com o servidor principal")
      os._exit(1)
  
  def getList(self):
    ...


  def cria_conexao_TCP(self):
    server = (self.HOST, self.PORT)
    
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      self.socket.bind(server)
    except:
      print("Bind falhou")
      os._exit(1)
    
    self.socket.listen(100)

  
  def aceita_conexao_rooms(self):
    while True:
      try: 
        client, client_address = self.socket.accept()
        thread = threading.Thread(target = self.controla_conexao, args = (client, ))
        thread.start()
      except:
        print("Falha ao aceitar conexão")
        os._exit(1)

  
  def checar_comando(self, client_socket):
    # Pega o comando recebido da Room
    message = client_socket.recv(1024).decode('utf-8')
    command = message.split(':')

    if command[0] == '/shutdown':
      
      self.socket.close()

    if command[0] == '/add_room':
      room = ':'.join(command[1:4])

      if not room in self.rooms_list:
        self.rooms_list.append(room)
        print(f"servidor: {room}")
    
    if command[0] == '/get_room':
      index = int(command[1])

      try:
        room = self.rooms_list[index].split(':')
        room = ':'.join(room[1:3])
        client_socket.send(f"{room}".encode('utf-8'))
      except IndexError:
        client_socket.send("error: opcao invalida".encode('utf-8'))

    if command[0] == '/get_room_id':
      message = len(self.rooms_list)
      client_socket.send(message.encode('utf-8'))

    if command[0] == '/list_rooms':
      rooms = []

      for index in range(len(self.rooms_list)):
        room_name = self.rooms_list[index].split(':')[0]
        rooms.append(f"{index} - {room_name}")

      rooms = '\n'.join(rooms)
      client_socket.send(f"{rooms}".encode('utf-8'))
      # print(f"{rooms}")

    if command[0] == '/close_room':
      del self.rooms_list[int(command[1])]
      print('Remover room na lista de rooms')



  def controla_conexao(self, client):
    # Controla a conexão da Room com o Server
    self.checar_comando(client)

  def fechar_servidor(self):
    self.socket.close()

server = Server('127.0.0.1', 5000)
server.run()

