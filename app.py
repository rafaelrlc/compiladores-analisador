from flask import Flask, request, jsonify
from flask_cors import CORS
from codigo import main2, executar

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/main', methods=['POST'])
def main():
    data = request.get_json()
    codigo = data['codigo']
    result = main2(codigo)
    data = {
        "token" : result[0],
        "browser" : result[1],
        "link" : result[2],
        "tempo" : result[3]
    }
    return jsonify(data), 200

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    arvore = data['arvore']
    print(arvore)
    executar(arvore)
    return "Success", 200

@app.route('/helloworld', methods=['POST'])
def get():
    data = request.get_json()
    print(data)
    return jsonify(data), 200