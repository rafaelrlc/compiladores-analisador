from flask import Flask, request, jsonify
from flask_cors import CORS
from codigo import main2, executar

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/main', methods=['POST'])
def main():
    try:
        data = request.get_json()
        codigo = data['codigo']
        result = main2(codigo)
        data = {
            "token": result[0],
            "browser": result[1],
            "link": result[2],
            "tempo": result[3]
        }
        return jsonify(data), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        arvore = data['arvore']
        print(arvore)
        executar(arvore)
        return "Success", 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

