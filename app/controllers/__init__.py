from flask import Blueprint

bp = Blueprint('base', __name__)

# 🔹 Importa as rotas associadas ao Blueprint
# - Isso garante que todas as rotas definidas no arquivo routes.py sejam carregadas.
from app.controllers import routes, api
