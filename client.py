import os
import socket
import sys
import threading

class Client:
  def __init__(self, host, port):
    self.HOST = host
    self.PORT = port

  def cria_conexao_tcp(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server = (self.HOST, self.PORT)
      self.socket.connect(server)
    except:
      print("Não foi possível encontrar sala")
      sys.exit()

  def enviar_mensagem(self):
    try:
      while True:
        msg = input()
        self.socket.send(msg.encode('utf-8'))

        if msg == '/exit': 
          print("Saindo do bate papo...")
          self.socket.close()
          os._exit(1)
    except:
      print("Ocorreu um erro")
      self.socket.close()
      os._exit(1)
  
  def receber_mensagem(self):
    while True:
      msg = self.socket.recv(2048).decode('utf-8')

      if msg == '/servidor_off': 
        print("Encerrando conexão...")
        self.socket.close()
        os._exit(1)

      print(msg)

  def run(self):
    self.cria_conexao_tcp()
    thread = threading.Thread(target = self.receber_mensagem)
    thread.start()
    self.enviar_mensagem()

# client = Client('127.0.0.1', 5000)
# client.run()





