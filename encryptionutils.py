from Crypto.Cipher import AES

key = b'ThisIsARandomKey'

def encrypt(data):
    return AES.new(key, AES.MODE_CFB, iv=key).encrypt(key+data)

def decrypt(data):
    # print('Before Decryption',data)
    d = AES.new(key, AES.MODE_CFB, iv=key).decrypt(data)
    if d[:len(key)]!=key:
        print(d,data)
        print('Decryption error!')
        return b''
    return d[len(key):]