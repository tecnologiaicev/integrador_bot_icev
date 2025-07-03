from flask import Blueprint, request, jsonify, current_app
import requests
from .auth import require_token
from requests.auth import HTTPBasicAuth
from app.controllers import bp


@bp.route("/singup", methods=["POST"])
@require_token
def consulta_dados():
    print("Corpo recebido:", request.data)

    dados_recebidos = request.json or {}

    cpf = dados_recebidos.get("cpf")
    if not cpf:
        return jsonify({"error": "CPF não fornecido no corpo da requisição"}), 400

    modulo_entidade = "API,00001"
    id_registro = "4"
    tipo = "S"

    base_url = current_app.config["BASE_URL"].rstrip("/")
    url = f"{base_url}/{modulo_entidade}/{id_registro}/{tipo}"
    
    params = {
        "parameters": f"CPF={cpf}"
    }

    user = current_app.config["USER"]
    senha = current_app.config["SENHA"]

    try:
        response = requests.get(url, params=params, auth=HTTPBasicAuth(user, senha))
        response.raise_for_status()
        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as err:
        return jsonify({
            "error": "Erro na requisição externa",
            "status_code": response.status_code,
            "detalhe": str(err),
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"error": "Erro interno", "detalhe": str(e)}), 500


@bp.route("/disciplina", methods=["POST"])
@require_token
def consulta_disciplina():
    print("Corpo recebido:", request.data)

    dados_recebidos = request.json or {}

    cpf = dados_recebidos.get("cpf")
    if not cpf:
        return jsonify({"error": "CPF não fornecido no corpo da requisição"}), 400

    modulo_entidade = "API,00002"
    id_registro = "4"
    tipo = "S"

    base_url = current_app.config["BASE_URL"].rstrip("/")
    url = f"{base_url}/{modulo_entidade}/{id_registro}/{tipo}"
    
    params = {
        "parameters": f"CPF={cpf}"
    }

    user = current_app.config["USER"]
    senha = current_app.config["SENHA"]

    try:
        response = requests.get(url, params=params, auth=HTTPBasicAuth(user, senha))
        response.raise_for_status()
        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as err:
        return jsonify({
            "error": "Erro na requisição externa",
            "status_code": response.status_code,
            "detalhe": str(err),
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        return jsonify({"error": "Erro interno", "detalhe": str(e)}), 500
