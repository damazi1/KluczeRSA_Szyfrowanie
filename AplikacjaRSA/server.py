from flask import Flask, request, jsonify

app = Flask(__name__)
stored_share = None

@app.route('/share', methods=['POST'])
def save_share():
    global stored_share
    stored_share = request.json.get('share')
    return jsonify({"message": "Udział zapisany pomyślnie"}), 200

@app.route('/share', methods=['GET'])
def get_share():
    if stored_share is not None:
        return jsonify({"share": stored_share}), 200
    return jsonify({"error": "Brak udziału na serwerze"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)