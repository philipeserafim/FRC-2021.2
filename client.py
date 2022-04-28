import os
import socket
import threading

class Client:
  def __init__(self, host, port):
    self.HOST = host
    self.PORT = port

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

    if (message.split(':'))[0] == '/get_room':
      return received_message
    else:
      print(received_message)

  
  def cria_conexao_tcp(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server = (self.HOST, self.PORT)
      self.socket.connect(server)
    except:
      print("Não foi possível encontrar sala")
      os._exit(0)

  def send_message_room(self):
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
      msg = self.socket.recv(4096).decode('utf-8')

      if msg == '/shutdown': 
        print("Encerrando conexão...")
        self.socket.close()
        os._exit(0)

      print(msg)


# client = Client('127.0.0.1', 5000)
# client.run()





