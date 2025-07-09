from flask import Blueprint, request, jsonify, current_app
from .auth import require_token
from requests.auth import HTTPBasicAuth
import requests
import time
from app.controllers import bp

# Sessão global de requests para reuso de conexão (melhora o desempenho)
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount("http://", adapter)
session.mount("https://", adapter)

def consultar_totvs(cpf, modulo_entidade):
    base_url = current_app.config["BASE_URL"].rstrip("/")
    id_registro = "4"
    tipo = "S"
    url = f"{base_url}/{modulo_entidade}/{id_registro}/{tipo}"
    params = {"parameters": f"CPF={cpf}"}

    user = current_app.config["USER"]
    senha = current_app.config["SENHA"]

    try:
        response = session.get(url, params=params, auth=HTTPBasicAuth(user, senha), timeout=2)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code

    except requests.exceptions.HTTPError as err:
        current_app.logger.error(f"Erro HTTP na chamada ao TOTVS: {err}")
        return jsonify({
            "error": "Erro na requisição externa",
            "status_code": response.status_code,
            "detalhe": str(err),
            "resposta": response.text
        }), response.status_code

    except Exception as e:
        current_app.logger.error(f"Erro inesperado na consulta TOTVS: {e}")
        return jsonify({"error": "Erro interno", "detalhe": str(e)}), 500


@bp.route("/singup", methods=["POST"])
@require_token
def consulta_dados():
    inicio = time.perf_counter()
    
    dados_recebidos = request.get_json(silent=True) or {}
    cpf = dados_recebidos.get("cpf")

    if not cpf:
        return jsonify({"error": "CPF não fornecido no corpo da requisição"}), 400

    resposta = consultar_totvs(cpf, "API,00001")

    fim = time.perf_counter()
    current_app.logger.info(f"/singup - Tempo total: {fim - inicio:.3f}s")

    return resposta


@bp.route("/disciplina", methods=["POST"])
@require_token
def consulta_disciplina():

    dados_recebidos = request.get_json(silent=True) or {}
    cpf = dados_recebidos.get("cpf")

    if not cpf:
        return jsonify({"error": "CPF não fornecido no corpo da requisição"}), 400

    resposta = consultar_totvs(cpf, "API,00002")



    return resposta
