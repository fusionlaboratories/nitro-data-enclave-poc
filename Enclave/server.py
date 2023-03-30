import socket
import ssl
import requests
import json
import boto3

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

        # Get data from AWS API call
        content = make_query(payload)

        # Send the response back to parent instance
        c.send(str.encode(json.dumps(content)))

        # Close the connection
        c.close() 

if __name__ == '__main__':
    main()