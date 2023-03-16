from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    print(data)
    result = a + b
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)