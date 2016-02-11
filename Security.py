from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import base64

class privateKey:
    key=None
    def __init__(self):
        random_generator = Random.new().read
        self.key = RSA.generate(1024, random_generator)

    def getPublicKey(self):
        return self.key.publickey()
        
    def Decryption(self,enc_data):
        return self.key.decrypt(enc_data)


class publicKey:
    key=None
    def __init__(self,publick):
        self.key = publick
 
    def Encryption(self,data):
        return self.key.encrypt(data,32)


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class AESCipher:
  
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))



iv = Random.new().read( 16 )
print iv
key="1234567812345678"
key=iv
AES1=AESCipher(key)
data="try"
Edata=AES1.encrypt(data)
print Edata
print AES1.decrypt(Edata)




##simple usage:
##    
##from Security import *
##privateK=privateKey()
##publicK=publicKey(privateK.getPublicKey())
##data="12345"
##enc_data=publicK.Encryption(data)
##dec_data=privateK.Decryption(enc_data)
##dec_data

    
