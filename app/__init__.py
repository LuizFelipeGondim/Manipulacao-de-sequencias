from flask import Flask
from core.indexer import InvertedIndex

# Inicia a aplicação e carrega o índice invertido na aplicação
def create_app():
    app = Flask(__name__)
    app.secret_key = "chave-super-secreta-e-unica" # Chave mockada pois o projeto não vai pra produção realmente
    
    indexer = InvertedIndex()
    app.config['INDEXER'] = indexer

    from .routes import main
    app.register_blueprint(main)

    return app