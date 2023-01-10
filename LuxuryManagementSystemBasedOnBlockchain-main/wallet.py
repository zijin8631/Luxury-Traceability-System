# coding:utf-8
import binascii
import base58
#this is an algorithm of the signature: ECDSA
from ecdsa import SigningKey, SECP256k1
from utils import hash_public_key, sum256_hex

class Wallet(object):
    #The hex version
    VERSION = b'\0'
    def __init__(self, private_key):
        #this is the private key
        self._private_key = private_key
        #from the private key to generate the public key
        self._public_key = private_key.get_verifying_key()
        self._address = ''
    
    @classmethod
    def generate_wallet(cls, curve=SECP256k1):
        """
        generate a wallet
        """
        #using the ECDSA algorithm which is imported from ecdsa package.
        sign_key = SigningKey.generate(curve=curve)
        return cls(sign_key)

    @property
    def private_key(self):
        #transfer to string type.
        return binascii.hexlify(self._private_key.to_string())
    
    @property
    def raw_private_key(self):
        return self._private_key

    @property
    def public_key(self):
        #transfer to string type.
        return binascii.hexlify(self._public_key.to_string()).decode()
    
    @property
    def address(self):
        #generate the address of the wallet
        if not self._address:
            #the value is the beginning of a zero with the hash_PU.
            prv_addr = self.VERSION + self._hash_public_key()
            #using base58 to encode the value above, get the address.
            self._address = base58.b58encode_check(prv_addr).decode()
        return self._address
    
    #transfer the value to string type.
    def _hash_public_key(self):
        return hash_public_key(self._public_key.to_string())

if __name__ == "__main__":
    w = Wallet.generate_wallet()
    print(w.address)
    