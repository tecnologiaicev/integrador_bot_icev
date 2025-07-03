from flask import request, jsonify, current_app

def require_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token não fornecido"}), 401

        expected_token = f"Bearer {current_app.config['API_TOKEN']}"
        
        if token != expected_token:
            return jsonify({"error": "Token inválido"}), 403

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
