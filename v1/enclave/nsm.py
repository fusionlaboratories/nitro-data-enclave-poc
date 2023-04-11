import base64
import Crypto.Hash.MD5 as MD5
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket
import ssl
import requests
import json
from OpenSSL import SSL

class NSMUtil():
    """NSM util class."""

    def __init__(self):
        """Construct a new NSMUtil instance."""


        # Generate a new RSA certificate, which will be used to
        # generate the Attestation document and to decrypt results
        # for KMS Decrypt calls with this document.
        self._rsa_key = RSA.generate(2048)
        self._public_key = self._rsa_key.publickey().export_key('DER')


 # Initialise NSMUtil
nsm_util = NSMUtil()
pub_key=nsm_util._public_key
dict={"key":pub_key}
print(json.dumps(str((dict))))

