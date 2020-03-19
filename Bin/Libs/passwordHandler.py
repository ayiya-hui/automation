import hashlib

class passwordHandler:
    """This class will handle the verification of an encrypted (MD5, SHA1 or SHA256)
    password."""
    def __init__(self, alg):
        if alg==1:
            self.hashHandler=hashlib.md5()
        elif alg==2:
            self.hashHandler=hashlib.sha1()
        elif alg==3:
            self.hashHandler=hashlib.sha256()

    def getHashCode(self, salt, password):
        """This method will take a salt and clear text password and return an encrypted
        hash."""
        self.hashHandler.update(salt+password)

        return self.hashHandler.hexdigest().upper()
