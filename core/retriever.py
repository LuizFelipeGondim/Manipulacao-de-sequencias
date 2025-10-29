import re
import math

class Retriever:
    def __init__(self, indexer, data_folder="data"):
        self.indexer = indexer
        self.data_folder = data_folder

    def process_query(self, query):
        tokens = self.tokenize(query)
        ast = self.parse(tokens)
        result_docs = self.evaluate(ast)
        ranked_results = self.rank_results(result_docs, query)
        return ranked_results

    def tokenize(self, query):
        pattern = r'\(|\)|AND|OR|[a-zA-Z0-9]+'
        tokens = re.findall(pattern, query)
        return tokens

    class Node:
        def __init__(self, value, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right

    def parse(self, tokens):
        def precedence(op):
            return 2 if op == "AND" else 1

        output = []
        operators = []

        for token in tokens:
            if token not in ("AND", "OR", "(", ")"):
                output.append(self.Node(token))
            elif token in ("AND", "OR"):
                while (operators and operators[-1] != "(" and
                       precedence(operators[-1]) >= precedence(token)):
                    op = operators.pop()
                    right = output.pop()
                    left = output.pop()
                    output.append(self.Node(op, left, right))
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    op = operators.pop()
                    right = output.pop()
                    left = output.pop()
                    output.append(self.Node(op, left, right))
                operators.pop()  # remove '('

        while operators:
            op = operators.pop()
            right = output.pop()
            left = output.pop()
            output.append(self.Node(op, left, right))

        return output[0] if output else None

    def evaluate(self, node):
        if node is None:
            return {}

        # Caso base: termo isolado
        if node.value not in ("AND", "OR"):
            results = self.indexer.search_word(node.value)
            if results is None:
                return {}
                
            return results

        # Caso recursivo: operador booleano
        left_results = self.evaluate(node.left)
        right_results = self.evaluate(node.right)

        if node.value == "AND":
            return {
                doc: left_results[doc] + right_results[doc]
                for doc in left_results if doc in right_results
            }

        elif node.value == "OR":
            union = dict(left_results)
            for doc, freq in right_results.items():
                union[doc] = union.get(doc, 0) + freq
            return union


    def rank_results(self, results, query):
        if not results:
            return []

        # Extrai os termos da consulta (ignorando operadores lógicos)
        terms = [t for t in re.findall(r"[a-zA-Z0-9]+", query) if t not in ("AND", "OR")]

        # Calcula média e desvio padrão por termo
        term_stats = {}
        for term in terms:
            docs = self.indexer.search_word(term)
            if not docs:
                continue
            freqs = list(docs.values())
            mean = sum(freqs) / len(freqs)
            var = sum((f - mean) ** 2 for f in freqs) / len(freqs)
            std = math.sqrt(var) if var > 0 else 1
            term_stats[term] = (mean, std, docs)

        if not term_stats:
            return []

        # Calcula score por documento
        scores = {}
        for doc, _ in results.items():
            term_scores = {}
            for term, (mean, std, docs) in term_stats.items():
                if doc in docs:
                    freq = docs[doc]
                    z = (freq - mean) / std
                    term_scores[term] = z

            if term_scores:
                # Termo mais relevante = maior z-score
                best_term = max(term_scores.items(), key=lambda x: x[1])[0]
                # Média dos z-scores (para o ranking geral)
                avg_score = sum(term_scores.values()) / len(term_scores)
                # Guarda score e termo mais relevante
                scores[doc] = (avg_score, best_term)

        # Ordena por score médio (decrescente)
        ranked_docs = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)

        # Gera snippets
        final_results = []
        for doc, (score, best_term) in ranked_docs:
            (snippet, title) = self._generate_snippet(doc, best_term)
            final_results.append((doc, snippet, title, score))

        return final_results



    def _generate_snippet(self, filename, term):
        try:
            path = f"{self.data_folder}/{filename}"
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            title = lines[0].strip() if lines else ""
            text = "".join(lines).strip()

            # Encontra a primeira ocorrência do termo (case-insensitive)
            pattern_search = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            match = pattern_search.search(text)
            if not match:
                return (text[:160] + "...", title)

            first_pos = match.start()

            # Cria o snippet com 80 caracteres antes e depois da ocorrência
            start = max(0, first_pos - 80)
            end = min(len(text), first_pos + len(term) + 80)
            snippet = text[start:end]

            # Destaca o termo no snippet (somente palavra inteira)
            snippet = pattern_search.sub(lambda m: f'<span class="highlight">{m.group(0)}</span>', snippet)

            # Adiciona reticências se necessário
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."

            return (snippet, title)

        except Exception:
            return "(snippet unavailable)"
