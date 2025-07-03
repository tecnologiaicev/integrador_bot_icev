from app.controllers import bp
from extensions import db
from flask import Flask, jsonify, request
from app.service.icev_digital_service import buscar_quiz, verify_token

@bp.route('/buscarquiz', methods=['GET'])
def select_dados():
    """
    Endpoint para buscar dados do quiz.

    Requer um token de autorização no cabeçalho da requisição.
    
    Parâmetros (query string):
    - `inicio` (str): Data inicial do período de busca (YYYY-MM-DD).
    - `fim` (str): Data final do período de busca (YYYY-MM-DD).
    - `id` (int): ID da disciplina.

    Retorno:
    - JSON com os dados do quiz (caso sucesso).
    - JSON com mensagem de erro (caso falha).
    """

    # 🔹 Obtém o token do cabeçalho da requisição
    auth_header = request.headers.get('Authorization')

    # Verifica se o token está presente
    if not auth_header:
        return jsonify({"message": "Token não fornecido"}), 401

    try:
        # Extrai apenas o token (removendo "Bearer " se presente)
        token = auth_header.split(" ")[-1]
    except IndexError:
        return jsonify({"message": "Formato do token inválido"}), 400

    # 🔹 Verifica se o token é válido
    if not verify_token(token):
        return jsonify({"message": "Token inválido"}), 403

    # 🔹 Obtém os parâmetros da query string
    data_inicio = request.args.get('inicio')  # Data de início
    data_fim = request.args.get('fim')  # Data de fim
    id_disc = request.args.get("id")  # ID da disciplina
    username = request.args.get("username")  # ID da disciplina
    # 🔹 Valida se os parâmetros necessários foram passados
    if not all([data_inicio, data_fim, id_disc]):
        return jsonify({"message": "Parâmetros 'inicio', 'fim' e 'id' são obrigatórios"}), 400

    # 🔹 Busca os dados no banco de dados
    dados = buscar_quiz(id_disc, data_inicio, data_fim,username)
    print("dados",dados)
    return dados  # Retorna os dados com status HTTP 200 (OK)
