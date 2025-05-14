
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_connection():
    return sqlite3.connect("lotes.db")

@app.route('/lotes', methods=['GET'])
def get_lotes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, lote, area_m2, status FROM lotes")
    lotes = [
        {"id": row[0], "lote": row[1], "area": row[2], "status": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(lotes)

@app.route('/lote/<int:lote_id>', methods=['PUT'])
def atualizar_lote(lote_id):
    data = request.get_json()
    novo_status = data.get("status")

    if novo_status not in ["Disponível", "Vendido"]:
        return jsonify({"error": "Status inválido"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM lotes WHERE id = ?", (lote_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Lote não encontrado"}), 404

    cursor.execute("UPDATE lotes SET status = ? WHERE id = ?", (novo_status, lote_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status atualizado com sucesso"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
