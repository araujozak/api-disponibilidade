from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def get_connection():
    caminho_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lotes.db")
    return sqlite3.connect(caminho_db)

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
    print("🔄 Dados recebidos:", data)  # Log de entrada

    novo_status = data.get("status")
    nova_area = data.get("area")

    if novo_status is not None and novo_status not in ["Disponível", "Vendido"]:
        return jsonify({"error": "Status inválido"}), 400

    if nova_area is not None:
        try:
            nova_area = float(nova_area)
            if nova_area <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "Área inválida"}), 400

    if novo_status is None and nova_area is None:
        return jsonify({"error": "Nenhuma alteração enviada"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM lotes WHERE id = ?", (lote_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Lote não encontrado"}), 404

    campos = []
    valores = []

    if novo_status is not None:
        campos.append("status = ?")
        valores.append(novo_status)

    if nova_area is not None:
        campos.append("area_m2 = ?")
        valores.append(nova_area)

    query = f"UPDATE lotes SET {', '.join(campos)} WHERE id = ?"
    valores.append(lote_id)

    print("📥 Query:", query)
    print("📦 Valores:", valores)

    cursor.execute(query, valores)
    conn.commit()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
