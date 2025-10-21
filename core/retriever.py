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
        print(result_docs)
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
            # agora já é um dict {"doc.txt": freq}
            return results

        # Caso recursivo: operador booleano
        left_results = self.evaluate(node.left)
        right_results = self.evaluate(node.right)

        if node.value == "AND":
            # Interseção: documentos presentes em ambos
            return {
                doc: left_results[doc] + right_results[doc]
                for doc in left_results if doc in right_results
            }

        elif node.value == "OR":
            # União: documentos presentes em pelo menos um
            union = dict(left_results)
            for doc, freq in right_results.items():
                union[doc] = union.get(doc, 0) + freq
            return union


    def rank_results(self, results, query):
        if not results:
            return []

        # Extrai os termos da consulta (ignorando operadores lógicos)
        terms = [t for t in re.findall(r"[a-zA-Z0-9]+", query) if t not in ("AND", "OR")]

        all_freqs = []
        for t in terms:
            docs = self.indexer.search_word(t)
            if docs:  # agora docs é um dict
                all_freqs.extend(docs.values())
        if not all_freqs:
            return []

        mean_freq = sum(all_freqs) / len(all_freqs)
        variance = sum((f - mean_freq) ** 2 for f in all_freqs) / len(all_freqs)
        std_dev = math.sqrt(variance) if variance > 0 else 1

        scores = {}
        for doc, total_freq in results.items():
            term_scores = {}
            for term in terms:
                term_docs = self.indexer.search_word(term)
                if not term_docs:
                    continue

                # term_docs é um dict, então acessamos direto a frequência
                if doc in term_docs:
                    freq = term_docs[doc]
                    z = (freq - mean_freq) / std_dev
                    term_scores[term] = z

            if term_scores:
                # Termo mais relevante = maior z-score
                best_term = max(term_scores.items(), key=lambda x: x[1])[0]
                # Média dos z-scores (para o ranking geral)
                avg_score = sum(term_scores.values()) / len(term_scores)
                # Guarda score e termo mais relevante
                scores[doc] = (avg_score, best_term)

        ranked_docs = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)

        final_results = []
        for doc, (score, best_term) in ranked_docs:
            snippet = self._generate_snippet(doc, [best_term])
            final_results.append((doc, score, snippet))

        return final_results


    def _generate_snippet(self, filename, terms_in_doc):
        try:
            path = f"{self.data_folder}/{filename}"
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            text_lower = text.lower()

            # Encontra a primeira ocorrência de qualquer termo
            first_pos = len(text)
            for term in terms_in_doc:
                pos = text_lower.find(term.lower())
                if pos != -1 and pos < first_pos:
                    first_pos = pos

            if first_pos == len(text):
                # Nenhum termo encontrado (por segurança)
                return text[:160] + "..."

            # Cria o snippet com 80 caracteres antes e depois da primeira ocorrência
            start = max(0, first_pos - 80)
            end = min(len(text), first_pos + 80)
            snippet = text[start:end]

            # Destaca todos os termos que aparecem no snippet
            for term in terms_in_doc:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                snippet = pattern.sub(f'<span class="highlight">{term}</span>', snippet)

            # Adiciona reticências se o snippet não estiver no início/fim do texto
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."

            return snippet

        except Exception:
            return "(snippet unavailable)"
