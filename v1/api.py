import json
import socket
import sys
from flask import Flask, jsonify, request

# initialize our Flask application
app= Flask(__name__)

@app.route("/host", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()
        return connectToEnclave(posted_data)

    

def connectToEnclave(payload):

    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    # Get CID from command line parameter
    cid = int(sys.argv[1])

    # The port should match the server running in enclave
    port = 5000

    # Connect to the server
    s.connect((cid, port))

    # send query to server running in enclave
    s.send(str.encode(json.dumps(payload)))
    result= (s.recv(16384).decode())

    # close the connection
    s.close()
    return result


#  main thread of execution to start the server
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)