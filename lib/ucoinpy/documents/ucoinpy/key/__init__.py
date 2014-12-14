'''
Ucoin public and private keys

@author: inso
'''

import base58
import base64
import scrypt
from nacl.signing import SigningKey as NaclSigningKey
from nacl.encoding import Base64Encoder


SEED_LENGTH = 32  # Length of the key
crypto_sign_BYTES = 64
SCRYPT_PARAMS = {'N': 4096,
                 'r': 16,
                 'p': 1
                 }


class SigningKey(NaclSigningKey):
    def __init__(self, password, salt):
        seed = scrypt.hash(password, salt,
                    SCRYPT_PARAMS['N'], SCRYPT_PARAMS['r'], SCRYPT_PARAMS['p'],
                    SEED_LENGTH)
        seedb64 = base64.b64encode(seed)
        super.__init__(seedb64, Base64Encoder)
        self.pubkey = Base58Encoder.encode(self.verify_key.key)


class Base58Encoder(object):
    @staticmethod
    def encode(data):
        return base58.b58encode(data)

    @staticmethod
    def decode(data):
        return base58.b58decode(data)
