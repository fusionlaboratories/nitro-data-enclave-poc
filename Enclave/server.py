import base64
import Crypto.Hash.MD5 as MD5
import socket
import ssl
import requests
import json
from NsmUtil import NSMUtil

def make_query(payload):
    
    hostname = payload['hostname']
    port = payload['port']

    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return {
                    'version': ssock.version(),
                    'peerCert': ssock.getpeercert()
                }

def main():
    print("Starting server...")

    # Initialise NSMUtil
    nsm_util = NSMUtil()
    
    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    # Listen for connection from any CID
    cid = socket.VMADDR_CID_ANY

    # The port should match the client running in parent EC2 instance
    port = 5000

    # Bind the socket to CID and port

    s.bind((cid, port))

    # Listen for connection from client
    s.listen()

    while True:
        c, addr = s.accept()

        # Get AWS credential sent from parent instance
        payload = json.loads((c.recv(4096)).decode())

        attestation_doc = nsm_util.get_attestation_doc()
        attestation_doc_b64 = base64.b64encode(attestation_doc).decode()
        c.send(str.encode({"public_key": nsm_util._public_key}))
        c.send(str.encode({"attestation_doc_b64": attestation_doc_b64}))

        # Get data from AWS API call
        content = make_query(payload)
        content_hash=MD5.new(content).digest()
        signature = nsm_util._rsa_key.sign(content_hash)
        result={
                "md5_hash":content_hash,
                "content":json.dumps(content),
                "signature":signature
                }
        # Send the response back to parent instance
        c.send(str.encode(result))

        # Close the connection
        c.close() 

if __name__ == '__main__':
    main()