import re
import math

class Retriever:
    def __init__(self, indexer, data_folder="data/sport"):
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
            results = self.indexer.pesquisarPalavra(node.value)
            if results is None:
                return {}
            # transforma lista de tuplas [(arquivo, freq)] em dict {arquivo: freq}
            return {doc: freq for doc, freq in results}

        # Caso recursivo: operador booleano
        left_results = self.evaluate(node.left)
        right_results = self.evaluate(node.right)

        if node.value == "AND":
            # Interseção: documentos presentes em ambos
            intersection = {
                doc: left_results[doc] + right_results[doc]
                for doc in left_results if doc in right_results
            }
            return intersection
        elif node.value == "OR":
            # União: documentos presentes em pelo menos um
            union = dict(left_results)
            for doc, freq in right_results.items():
                union[doc] = union.get(doc, 0) + freq
            return union

    def rank_results(self, results, query):
        if not results:
            return []

        terms = [t for t in re.findall(r"[a-zA-Z0-9]+", query) if t not in ("AND", "OR")]
        scores = {}

        # Calcula médias e desvios no corpus
        all_freqs = []
        for t in terms:
            docs = self.indexer.pesquisarPalavra(t)
            if docs:
                all_freqs.extend([freq for _, freq in docs])
        if not all_freqs:
            return []

        mean_freq = sum(all_freqs) / len(all_freqs)
        variance = sum((f - mean_freq)**2 for f in all_freqs) / len(all_freqs)
        std_dev = math.sqrt(variance) if variance > 0 else 1

        # Para cada documento do resultado, calcula média dos z-scores
        for doc, total_freq in results.items():
            term_scores = []
            terms_in_doc = []  # lista dos termos que realmente aparecem no doc
            for term in terms:
                term_docs = self.indexer.pesquisarPalavra(term)
                if not term_docs:
                    continue
                freq_dict = dict(term_docs)
                if doc in freq_dict:
                    z = (freq_dict[doc] - mean_freq) / std_dev
                    term_scores.append(z)
                    terms_in_doc.append(term)  # só adiciona se termo realmente ocorre no doc
            if term_scores:
                avg_score = sum(term_scores) / len(term_scores)
                scores[doc] = (avg_score, terms_in_doc)  # agora guardamos os termos do doc

        # Ordena por relevância decrescente
        ranked_docs = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)

        # Gera snippets para os top documentos
        final_results = []
        for doc, (score, terms_in_doc) in ranked_docs:
            snippet = self._generate_snippet(doc, terms_in_doc)
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
