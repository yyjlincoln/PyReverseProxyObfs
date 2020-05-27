from connutils import TCPHandler
from encryptionutils import encrypt, decrypt

def redirection_mapping(sx, addr):
    raw = sx.recv(2048) # Receive request
    


TCPHandler(('0.0.0.0',80),redirection_mapping)