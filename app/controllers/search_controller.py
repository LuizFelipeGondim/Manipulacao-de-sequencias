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

        # Verifica se ha espaco entre os parenteses e os outros termos
        if "(" in processed_tokens or ")" in processed_tokens:
            raise ValueError("Consulta inválida: Não é aceito espaço entre '(' ou ')' e uma palavra/conector.")

        # Verifica se a query inicia ou termina com algum conector logico
        if processed_tokens[0] in logical_ops or processed_tokens[-1] in logical_ops:
            raise ValueError("Consulta inválida: Conectores lógicos não podem iniciar ou finalizar consultas.")

        # Percorre tokens para validar estrutura
        for i in range(len(processed_tokens) - 1):
            curr, nxt = processed_tokens[i], processed_tokens[i + 1]

            # Caso 1: duas palavras seguidas sem operador lógico
            if (
                curr not in logical_ops and curr not in {"(", ")"}
                and nxt not in logical_ops and nxt not in {"(", ")"}
            ):
                raise ValueError(
                    f"Consulta inválida: '{curr}' e '{nxt}' sem operador lógico entre elas."
                )

            # Caso 2: dois operadores lógicos seguidos
            if curr in logical_ops and nxt in logical_ops:
                raise ValueError(
                    f"Consulta inválida: operadores '{curr}' e '{nxt}' consecutivos."
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
            score = doc_info[3]

            self.results.append({
                "category": filename.split('.')[0][4:],
                "filename": filename,
                "snippet": snippet,
                "title": title,
                "score": score
            })

        return {"results": self.results, "error": error_message}
