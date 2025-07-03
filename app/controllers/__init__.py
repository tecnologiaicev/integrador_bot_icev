from flask import Blueprint

# 🔹 Criação do Blueprint 'base'
# - O primeiro argumento ('base') é o nome do Blueprint.
# - O segundo argumento (__name__) informa onde esse Blueprint está definido.
bp = Blueprint('base', __name__)

# 🔹 Importa as rotas associadas ao Blueprint
# - Isso garante que todas as rotas definidas no arquivo routes.py sejam carregadas.
from app.controllers import routes, api
