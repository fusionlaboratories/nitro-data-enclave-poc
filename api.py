from flask import Flask, jsonify, request

# initialize our Flask application
app= Flask(__name__)

@app.route("/host", methods=["POST"])
def setName():
    if request.method=='POST':
        posted_data = request.get_json()
        data = posted_data['data']
        return jsonify(str("Successfully stored  " + str(data)))