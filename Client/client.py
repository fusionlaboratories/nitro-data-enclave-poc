import sys
import socket
import requests
import json


def main():

    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    
    # Get CID from command line parameter
    cid = int(sys.argv[1])

    # The port should match the server running in enclave
    port = 5000

    # Connect to the server
    s.connect((cid, port))

    # send query to server running in enclave
    package = ["binance.com",443]
    s.send(str.encode(json.dumps(package)))
    
    # receive data from the server
    print(s.recv(1024).decode())

    # close the connection 
    s.close()

if __name__ == '__main__':
    main()