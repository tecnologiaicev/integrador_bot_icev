from flask import Flask
from config import Config
from extensions import db 
from sqlalchemy import text

def create_app(config_class=Config, debug=True):
    app = Flask(__name__)
    app.config.from_object(config_class)
    print(":: Iniciando banco de dados...")
    db.init_app(app)
    
    with app.app_context():
        try:
            db.session.execute(text('SELECT * FROM icev_course LIMIT 1'))
            print(":: Banco de dados conectado com sucesso!")
        except Exception as e:
            print(e)

    from app.controllers import bp as std_bp
    app.register_blueprint(std_bp, url_prefix='/base')


    return app