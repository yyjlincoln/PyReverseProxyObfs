from connutils import TCPHandler, pack, unpack
from encryptionutils import encrypt, decrypt
import json

conf = {
    # Distingush "address" "serveraddress" "localaddress"
    'address':'play.extremecraft.net',
    'port':80,
    'localaddress':'localhost',
    'localport':8081,
    'serveraddress':'stream.mcsrv.icu',
    'serverport':80
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
    # Send the configuration to the server at the start of each connection
    sx.send(encrypt(pack(3,json.dumps({
        'address':conf['address'],
        'port':conf['port']
    }).encode())))
    # Returns the server's address
    return (conf['serveraddress'],conf['serverport']), sendproc, recvproc # Addr, recvproc, sendproc

TCPHandler((conf['localaddress'],conf['localport']),redirection_mapping)