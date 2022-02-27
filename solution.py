from socket import *

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"
     
    # Create socket called clientSocket and establish a TCP connection with mailserver and port
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(("127.0.0.1", port))
    recv = clientSocket.recv(1024).decode()

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()

    # Send MAIL FROM command and print server response.
    MAILFROM = "Mail From: <ashiq08401@gmail.com> \r\n"
    clientSocket.send(MAILFROM.encode())
    recv2 = clientSocket.recv(1024).decode()

    # Send RCPT TO command and print server response.
    RCPTTO = "RCPT To: <ashiq08401@gmail.com> \r\n"
    clientSocket.send(RCPTTO.encode())
    recv3 = clientSocket.recv(1024).decode()

    # Send DATA command and print server response.
    DATA = "DATA\r\n"
    clientSocket.send(DATA.encode())
    recv4 = clientSocket.recv(1024).decode()

    # Send message data.
    clientSocket.send(msg.encode())
    clientSocket.send(endmsg.encode())
    recv5 = clientSocket.recv(1024).decode()

    # Message ends with a single period.
    #clientSocket.send(endmsg.encode())
    #recv6 = clientSocket.recv(1024).decode()

    # Send QUIT command and get server response.
    QUIT = "QUIT\r\n"
    clientSocket.send(QUIT.encode())
    recv7 = clientSocket.recv(1024).decode()
    clientSocket.close()


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
