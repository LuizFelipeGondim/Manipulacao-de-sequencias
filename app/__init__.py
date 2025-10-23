from flask import Flask
from core.indexer import InvertedIndex

def create_app():
    app = Flask(__name__)
    app.secret_key = "chave-super-secreta-e-unica"
    
    indexer = InvertedIndex()
    app.config['INDEXER'] = indexer

    from .routes import main
    app.register_blueprint(main)

    return app