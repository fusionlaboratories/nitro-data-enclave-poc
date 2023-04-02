import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import socket
import ssl
import json
from NsmUtil import NSMUtil

def make_query(payload):

    hostname = payload['hostname']
    port = payload['port']
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return {
                        'version': ssock.version(),
                        'peerCert': ssock.getpeercert()
                    }
    except: 
        return {}

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

        #c.sendall(str.encode(json.dumps({"public_key": str(nsm_util._public_key)})))
        #c.sendall(str.encode(json.dumps({"attestation_doc_b64": attestation_doc_b64})))

        # Get data from AWS API call
        content = make_query(payload)
        h = SHA256.new()
        h.update(json.dumps(content, sort_keys=True).encode())
        signature = pkcs1_15.new(nsm_util._rsa_key).sign(h)
        result={
                #"sha256_hash":content_hash,
                "content":json.dumps(content),
                "signature_b64":base64.b64encode(signature).decode(),
                "public_key": str(nsm_util._public_key),
                "attestation_doc_b64": attestation_doc_b64
                }
        # Send the response back to parent instance
        c.sendall(str.encode(json.dumps(result, sort_keys=True)))

        # Close the connection
        c.close()

if __name__ == '__main__':
    main()
                                     