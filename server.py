from connutils import TCPHandler, pack, unpack
from encryptionutils import encrypt, decrypt
import json

def recvproc(data):
    try:
        msgtype, data = unpack(decrypt(data))
    except:
        print('Exception')
        return None

    if msgtype==1:
        # TCP, pass to default handler
        return data
    elif msgtype==2:
        # UDP
        print('UDP is currently not supported')
    elif msgtype==3:
        print('Control Message')

def sendproc(data):
    return encrypt(pack(1, data))

def redirection_mapping(sx, addr):
    try:
        raw = decrypt(sx.recv(2048)) # Receive redirection request
        datatype, data = unpack(raw)
    except Exception as e:
        sx.send(b'''HTTP/1.1 403 Forbidden\r\n\r\n''')
        # print(e)
        raise e
        return False, None, None
    
    if datatype!=3:
        print('First datatype must be CTL.')
        
        sx.send(b'''HTTP/1.1 403 Forbidden\r\n\r\n''')

        return False, None, None # Shuts connection
    conf = json.loads(data)
    print('CONFIG',conf)
    return (conf['address'],conf['port']), sendproc, recvproc # Addr, recvproc, sendproc

TCPHandler(('0.0.0.0',80),redirection_mapping)