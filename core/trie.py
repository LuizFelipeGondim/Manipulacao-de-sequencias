import json
import os

# Representa um no de uma Trie.
class CompactNode:
    def __init__(self):
        self.children = {}
        self.occurrences = {}
        self.end_of_word = False

# Classe responsavel por montar, salvar e ler em disco e consultar palavras na Trie 
class CompactTrie:
    def __init__(self):
        self.root = CompactNode()

    # Insere na Trie a palavra informada, se ela já estiver na estrutura, sua ocorrência é incrementada no documento especificado. 
    def insert_word(self, word, document_name):
        node = self.root
        while word:
            has_common_prefix = False

            for key in list(node.children.keys()):
                common_prefix = self._common_prefix(key, word)
                if common_prefix:
                    # Caso 1: O prefixo é igual à chave existente.
                    if common_prefix == key:
                        node = node.children[key]
                        word = word[len(common_prefix):]
                        has_common_prefix = True
                        break
                    # Caso 2: O prefixo é apenas parte da chave
                    else:
                        existing_node = node.children.pop(key)
                        new_node = CompactNode()

                        new_node.children[key[len(common_prefix):]] = existing_node
                        new_node.end_of_word = existing_node.end_of_word and (key[len(common_prefix):] == "")
                        node.children[common_prefix] = new_node
                        node = new_node
                        word = word[len(common_prefix):]
                        has_common_prefix = True
                        break

            if has_common_prefix == False:
                new_node = CompactNode()
                new_node.end_of_word = True
                if document_name not in new_node.occurrences:
                    new_node.occurrences[document_name] = 1
                else:
                    new_node.occurrences[document_name] += 1
                node.children[word] = new_node
                return

        # Marque o fim da palavra
        node.end_of_word = True
        if document_name not in node.occurrences:
            node.occurrences[document_name] = 1
        else:
            node.occurrences[document_name] += 1

    # Consulta na Trie a palavra informada.
    def search_word(self, word):
        node = self.root
        while word:
            found = False
            for key, child in node.children.items():
                if word.startswith(key):  # checks if key is a prefix of word
                    word = word[len(key):]
                    node = child
                    found = True
                    break

            if not found:
                return {}

        return node.occurrences

    # 
    def _common_prefix(self, a, b):
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return a[:i]

    # Salva a Trie no disco em formato JSON.
    def save_to_disk(self, file_path):
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True) 
        
        structure = self._node_to_dict(self.root)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(structure, f, ensure_ascii=False, indent=2)
        print(f"Trie saved to {file_path}")

    # Carrega a Trie salva no disco.
    def load_from_disk(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            structure = json.load(f)
        self.root = self._dict_to_node(structure)
        print(f"Trie loaded from {file_path}")

    # ================================================================
    # Funções auxiliares
    # ================================================================

    # Converte recursivamente um nó em um dicionário serializável em JSON.
    def _node_to_dict(self, node):
        return {
            "end_of_word": node.end_of_word,
            "occurrences": node.occurrences,
            "children": {key: self._node_to_dict(child) for key, child in node.children.items()}
        }

    # Converte um dicionário de volta em um objeto CompactNode.
    def _dict_to_node(self, dictionary):
        node = CompactNode()
        node.end_of_word = dictionary["end_of_word"]
        node.occurrences = dictionary["occurrences"]
        for key, sub_node in dictionary["children"].items():
            node.children[key] = self._dict_to_node(sub_node)
        return node
