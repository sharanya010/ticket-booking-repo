from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"service":"ticket-booking", "status":"ok"})

@app.route('/book', methods=['POST'])
def book():
    data = request.json or {}
    name = data.get('name', 'anonymous')
    seats = data.get('seats', 1)
    return jsonify({"message": f"Booked {seats} seats for {name}"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
