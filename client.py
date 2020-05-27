from connutils import TCPHandler, pack, unpack
from encryptionutils import encrypt, decrypt
import json

header = '''POST /stream HTTP/1.1\r\n\r\n'''

conf = {
    # Distingush "address" "serveraddress" "localaddress"
    'address':input('Please input the ip address of the server>'),
    'port':25565,
    'localaddress':'localhost',
    'localport':25565,
    'serveraddress':'stream.mcsrv.icu',
    'serverport':80
}

# When the data is too big, the packet is transferred
# in multiple packets so it will cause decryption error.

# Solution: Get another layer of package

def sendproc(data):
    data = data.split('\r\n\r\n')[-1]
    data = decrypt(data)
    # if msgtype==1:
    #     # TCP, pass to default handler
    #     return data
    # elif msgtype==2:
    #     # UDP
    #     print('UDP is currently not supported')
    # elif msgtype==3:
    #     print('Control Message')
    return data

def sendconfig(sx,dest):
    # Send the configuration to the server at the start of each connection
    # CTL was sent to the wrong request
    print('Sent CTL')
    
    dest.send(encrypt(json.dumps({
        'address':conf['address'],
        'port':conf['port']
    }).encode()))

def recvproc(data):
    # Receive message from local & excrypt to transfer to the server
    return header+encrypt(data)

def redirection_mapping(sx, addr):
    # Returns the server's address
    return (conf['serveraddress'],conf['serverport']), sendproc, recvproc # Addr, recvproc, sendproc

TCPHandler((conf['localaddress'],conf['localport']),redirection_mapping, sendconfig)