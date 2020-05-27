from connutils import TCPHandler, pack, unpack
from encryptionutils import encrypt, decrypt
import json

conf = {
    'address':'play.extremecraft.net',
    'port':25565
}

def sendproc(data):
    msgtype, data = unpack(decrypt(data))
    if msgtype==1:
        # TCP, pass to default handler
        return data
    elif msgtype==2:
        # UDP
        print('UDP is currently not supported')
    elif msgtype==3:
        print('Control Message')

def recvproc(data):
    # Receive message from local & excrypt to transfer to the server
    return encrypt(pack(1, data))

def redirection_mapping(sx, addr):
    sx.send(json.dumps(conf)) # Send the configuration to the server at the start of each connection
    return (conf['address'],conf['port']), recvproc, sendproc # Addr, recvproc, sendproc

TCPHandler(('localhost',25565),redirection_mapping)