from core.retriever import Retriever
from flask import current_app
import os

class SearchController:
    def __init__(self):
        self.results = []

    def _process_query_string(self, query):
        query = query.strip()
        tokens = query.split()

        processed_tokens = []
        logical_ops = {"AND", "OR"}

        for token in tokens:
            if token in logical_ops:
                processed_tokens.append(token)
            else:
                processed_tokens.append(token.lower())

        # Verifica se contém apenas conectores lógicos
        if all(t in logical_ops for t in processed_tokens):
            raise ValueError("Consulta inválida: contém apenas conectores lógicos.")

        # Verifica se há duas palavras seguidas sem operador lógico
        for i in range(len(processed_tokens) - 1):
            if (
                processed_tokens[i] not in logical_ops
                and processed_tokens[i + 1] not in logical_ops
            ):
                raise ValueError(
                    f"Consulta inválida: '{processed_tokens[i]}' e '{processed_tokens[i+1]}' sem operador lógico entre elas."
                )

        return " ".join(processed_tokens)

    def searchResults(self, query):
        self.results = []
        error_message = None

        try:
            query_processed = self._process_query_string(query)
        except ValueError as e:
            return {"results": [], "error": str(e)}
        except Exception:
            return {"results": [], "error": "Erro ao processar a consulta."}

        try:
            retriever = Retriever(current_app.config['INDEXER'], "data")
            retrieved_docs = retriever.process_query(query_processed)
        except Exception as e:
            return {"results": [], "error": f"Erro ao buscar resultados"}

        for doc_info in retrieved_docs:
            filename = doc_info[0]
            snippet = doc_info[1]
            title = doc_info[2]

            self.results.append({
                "category": filename.split('.')[0][4:],
                "filename": filename,
                "snippet": snippet,
                "title": title
            })

        return {"results": self.results, "error": error_message}
