@app.route('/lote/<int:lote_id>', methods=['PUT'])
def atualizar_lote(lote_id):
    data = request.get_json()
    novo_status = data.get("status")
    nova_area = data.get("area")

    if novo_status not in ["Disponível", "Vendido"]:
        return jsonify({"error": "Status inválido"}), 400

    if not isinstance(nova_area, (int, float)):
        return jsonify({"error": "Área inválida"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM lotes WHERE id = ?", (lote_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Lote não encontrado"}), 404

    cursor.execute("UPDATE lotes SET status = ?, area_m2 = ? WHERE id = ?", (novo_status, nova_area, lote_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status e área atualizados com sucesso"}), 200
