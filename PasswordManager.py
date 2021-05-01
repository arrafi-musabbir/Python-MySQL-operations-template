from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64


class PasswordManager:
    
    def __init__(self):
        self.salt = self.retrieveSalt()
        
    def generateSalt(self):
        salt = os.urandom(32)
        path = '.salt'
        # default salt
        # salt = b'\x02\x90/\xef\xc75\x807A\xe5d\xcf\x9c\xae\xbdL/\xbd+\x07\xbb\xc5\x81\xdb\xb4\xbbJ\xac*~\xc6\x0c'
        with open(path, 'wb') as file:
            file.write(salt)
        return salt
    
    def retrieveSalt(self):
        with open(os.path.join(os.getcwd(),'.salt'), 'rb') as file:
            return file.read()

    def generateKey(self, passphrase):
        
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=self.salt,
        iterations=1000,
        backend=default_backend()
    )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
        
    def encrypt(self):
        
        
    
    
    
if __name__ == '__main__':
    # salt = b'\x02\x90/\xef\xc75\x807A\xe5d\xcf\x9c\xae\xbdL/\xbd+\x07\xbb\xc5\x81\xdb\xb4\xbbJ\xac*~\xc6\x0c'
    a = PasswordManager()  
    print(type(a.retrieveSalt()))
    print(a.generateKey('alphadeltafoxtrot'))          