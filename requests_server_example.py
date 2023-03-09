from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    print(data)
    return jsonify({'response': 'Hello, {}!'.format(data)})

if __name__ == '__main__':
    app.run(port=8000)

