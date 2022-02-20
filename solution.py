from socket import *
import sys


def webServer(port=13331):

  serverSocket = socket(AF_INET, SOCK_STREAM)
 
  serverSocket.bind(("localhost", port)) 

  serverSocket.listen(1)


  while True:
    connectionSocket, addr = serverSocket.accept()
    try:
      try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        messageok = 'HTTP/1.1 200 OK \r\n'
        connectionSocket.send(messageok.encode())

        #Send file 
        for i in range(0, len(outputdata)):
          connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
      except IOError:

        # handle file not found (404)
        messageNotOk = 'HTTP/1.1 404 Not Found\n\n'
        connectionSocket.send(messageNotOk.encode())

        connectionSocket.close()

    except (ConnectionResetError, BrokenPipeError):
      pass

  serverSocket.close()
  sys.exit()

if __name__ == "__main__":
  webServer(13331)
