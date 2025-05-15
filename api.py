@app.route('/lote/<int:lote_id>', methods=['PUT'])
def atualizar_lote(lote_id):
    data = request.get_json()

    novo_status = data.get("status")
    nova_area = data.get("area")

    # Validações apenas se os campos forem enviados
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

    # Verifica se o lote existe
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
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

    return jsonify({"success": True})
