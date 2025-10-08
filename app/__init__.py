from flask import Flask
from core import Indexer, Retriever

def create_app():
    app = Flask(__name__)

    indexer = Indexer()
    retriever = Retriever()

    # carrega data e constroi índice

    # app.config['INDEXER'] = indexer
    # app.config['RETRIEVER'] = retriever
    # app.config['DATA'] = data

    from .routes import main
    app.register_blueprint(main)

    return app