from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64
import yaml
import cryptography.fernet

class PasswordManager:
    
    def __init__(self, passphrase):
        self.encryptiontype = cryptography.fernet.Fernet(self.generateKey(passphrase, self.retrieveSalt()))
        
    def generateSalt(self):
        salt = os.urandom(32)
        path = '.salt'
        # default salt
        # salt = b'\x02\x90/\xef\xc75\x807A\xe5d\xcf\x9c\xae\xbdL/\xbd+\x07\xbb\xc5\x81\xdb\xb4\xbbJ\xac*~\xc6\x0c'
        with open(path, 'wb') as file:
            file.write(salt)
        return salt
    
    def retrieveSalt(self):
        try:
            with open(os.path.join(os.getcwd(),'.salt'), 'rb') as file:
                return file.read()
        except FileNotFoundError:
            salt = b'\x02\x90/\xef\xc75\x807A\xe5d\xcf\x9c\xae\xbdL/\xbd+\x07\xbb\xc5\x81\xdb\xb4\xbbJ\xac*~\xc6\x0c'
            return salt

    def generateKey(self, passphrase, salt):
        
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    
    def retrieveServerCredentials(self):
        serverCreds = dict()
        try:
            with open(os.path.join(os.getcwd(),'creds.yml'), 'r') as file:
                yaml_data = yaml.safe_load(file)
                for key in yaml_data:
                    serverCreds[self.encryptiontype.decrypt(key).decode()] = self.encryptiontype.decrypt(yaml_data[key]).decode()
            return serverCreds 
        except cryptography.fernet.InvalidToken:
            print("Wrong passphrase")
            return False
    
    def encryptServerCredentials(self):
        with open(os.path.join(os.getcwd(),'creds.yml'), 'r') as file:
            yaml_data = yaml.safe_load(file)
        serverCreds = dict()
        with open(os.path.join(os.getcwd(),'creds.yml'), 'w') as file:
            for key in yaml_data:
                serverCreds[self.encryptiontype.encrypt(key.encode())] = self.encryptiontype.encrypt(yaml_data[key].encode())
            yaml.dump(serverCreds, file)
        print("Server credentials encrypted and stored successfully")
    
if __name__ == '__main__':
    # replace passphrase with your passphrase
    a = PasswordManager("passphrase")
    # a.retrieveServerCredentials()
    # a.encryptServerCredentials()   
    
    
    
# default salt used in here
# salt = b'\x02\x90/\xef\xc75\x807A\xe5d\xcf\x9c\xae\xbdL/\xbd+\x07\xbb\xc5\x81\xdb\xb4\xbbJ\xac*~\xc6\x0c'