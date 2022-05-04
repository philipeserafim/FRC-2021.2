from concurrent.futures import thread
import os
import socket
import sys
import threading
import time

class Client:
  def __init__(self, host, port):
    self.HOST = host
    self.PORT = port
    self.stop = False
    

  def start_room(self):
    # Cria conexao TCP
    self.cria_conexao_tcp()

    # Roda uma thread para ficar escutando as mensagens que o client receber
    thread = threading.Thread(target = self.receber_mensagem)
    thread.start()

    # Envia mensagens na thread principal
    self.send_message_room()

  def send_to_server(self, message):
    # Cria conexao TCP
    self.cria_conexao_tcp()

    self.socket.send(message.encode('utf-8'))
    received_message = self.socket.recv(4096).decode('utf-8')
    self.socket.close()

    if (message.split(':'))[0] == '/get_room' and received_message != 'error: opcao invalida':
      return received_message
    else:
      print(received_message)

  
  def cria_conexao_tcp(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server = (self.HOST, self.PORT)
      self.socket.connect(server)
    except Exception as e:
      print(e)
      print("Não foi possível encontrar sala")
      sys.exit()

  def send_message_room(self):
    try:
      while True:
        msg = input()
        self.socket.send(msg.encode('utf-8'))

        if msg == '/shutdown': 
          print("Saindo do bate papo...")
          self.socket.close()
          os._exit(1)
    except:
      self.socket.send("/exit".encode('utf-8'))
      self.socket.close()
      os._exit(1)
  
  def receber_mensagem(self):
    try: 
      while True:
        msg = self.socket.recv(4096).decode('utf-8')

        if msg == '/shutdown': 
          print("Encerrando conexão...")
          self.socket.close()
          os._exit(1)
        print(msg)
  
    except: 
      print("Encerrando conexão...")
      self.socket.close()
      os._exit(1)


# client = Client('127.0.0.1', 5000)
# client.run()





