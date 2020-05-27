import socket
import struct
import threading

def pack(datatype, data):
    '''
    Data Types:
        0: TCP
        1: UDP
        2: CTL (Configuration)
    
    General Outline:

    [Data Type i (4)] + [Data ?s (?)]

    Controlling:

    [2] [{jsondata}]
    '''
    Packed = struct.pack('i'+str(len(data))+'s', datatype, data)
    return Packed

def unpack(packed):
    '''
    Returns DataType, Data
    '''
    Calc=len(packed)-struct.calcsize('i')
    DataType, Data = struct.unpack('i'+str(Calc)+'s',packed)
    return DataType, Data

def TCPHandler(bindaddress, redirection_address, before_transfer = None):
    '''redirection_address should be a function, and it should take in socket, addr and return address tuple or None.'''
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.bind(bindaddress)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    so.listen(10)
    while True:
        sx, addr = so.accept()
        taph = threading.Thread(target=TCPHandlerPreConnection,args=(sx, addr, redirection_address), kwargs={'before_transfer':before_transfer})
        taph.setDaemon(True)
        taph.start()

def TCPHandlerPreConnection(sx, addr, redirection_address, before_transfer = None):
    destaddr, recvproc, sendproc  = redirection_address(sx, addr)
    if isinstance(destaddr, tuple):
        try:
            dest = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            dest.connect(destaddr)
        except:
            print('Can not establish connection to address',destaddr,'!')
            try:
                sx.shutdown(socket.SHUT_RDWR)
            except:
                pass
            sx.close()
            return
        
        if callable(before_transfer):
            before_transfer(sx, dest)
                
        
        print('Starting f2t thread...')
        f2t = threading.Thread(target=TCPHandlerWorker, args=(sx, dest, sendproc))
        print('Starting t2f thread...')
        t2f = threading.Thread(target=TCPHandlerWorker, args=(dest, sx, recvproc))
        f2t.setDaemon(True)
        t2f.setDaemon(True)
        f2t.start()
        t2f.start()      
    elif destaddr==None:
        print('Warning: Connnection is not handled by the default handler.')
    elif destaddr==False:
        print('Warning: Disconnecting both sockets')
        try:
            sx.shutdown(socket.SHUT_RDWR)
        except:
            pass

        sx.close()
    else:
        print('Invalid destaddr!')

        

def TCPHandlerWorker(fromhand, tohand, proc):
    while True:
        try:
            data = fromhand.recv(2048)
            if data==b'':
                print('Connection Reset!')
                try:
                    fromhand.shutdown(socket.SHUT_RDWR)
                    tohand.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                fromhand.close()
                tohand.close()
                return
            data = proc(data)
            print('ABOUT',data)
            if data:
                tohand.send(data)
                print('Data transferred to tohand!')
        except Exception as e:
            print('Broken Connection:',e)
            return
    
