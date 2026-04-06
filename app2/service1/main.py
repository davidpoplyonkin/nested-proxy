from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "Message": "Service 1, App 2"
    })

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
