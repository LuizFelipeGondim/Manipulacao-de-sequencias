import json



class NoCompacto:
    def __init__(self):
        self.filhos={}
        self.aparicoes={}
        self.fim_palavra = False

class TrieCompacta:
    def __init__(self):
        self.raiz = NoCompacto()

    def inserirPalavra(self, palavra, nome_documento):
        no = self.raiz
        while palavra:
            teve_prefixo_comum = False

            for chave in list(no.filhos.keys()):
                prefixo_comum = self._prefixo_comum(chave, palavra)
                if prefixo_comum:
                    # Caso 1: o prefixo é igual à chave existente
                    if prefixo_comum == chave:
                        no = no.filhos[chave]
                        palavra = palavra[len(prefixo_comum):]
                        teve_prefixo_comum = True
                        break
                    # Caso 2: o prefixo é apenas parte da chave
                    else:
                        # Divide o nó existente
                        no_existente = no.filhos.pop(chave)                                #####
                        novo_no = NoCompacto()
                        
                        novo_no.filhos[chave[len(prefixo_comum):]] = no_existente
                        novo_no.fim_palavra = no_existente.fim_palavra and (chave[len(prefixo_comum):] == "")
                        no.filhos[prefixo_comum] = novo_no
                        no = novo_no
                        palavra = palavra[len(prefixo_comum):]
                        teve_prefixo_comum = True
                        break
                    
            if teve_prefixo_comum == False:                                                
                # Nenhum prefixo em comum 
                novo_no = NoCompacto()
                novo_no.fim_palavra = True
                if nome_documento not in novo_no.aparicoes:
                    novo_no.aparicoes[nome_documento] = 1
                else : novo_no.aparicoes[nome_documento] += 1
                no.filhos[palavra] = novo_no
                return

        # Marca o fim da palavra
        no.fim_palavra = True
        if nome_documento not in no.aparicoes:
            no.aparicoes[nome_documento] = 1
        else : no.aparicoes[nome_documento] += 1

    def buscarPalavra(self, palavra):
        no = self.raiz
        while palavra:
            encontrado = False
            for chave, filho in no.filhos.items():
                if palavra.startswith(chave):           # verifica se chave é prefixo de palavra
                    palavra = palavra[len(chave):]
                    no = filho
                    encontrado = True
                    break
            if not encontrado:
                print('Essa palavra não tem em nenhum arquivo')
                return False
        print(no.aparicoes)

    
    def _prefixo_comum(self, a, b):
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return a[:i]


    def exibir(self, no=None, prefixo=""):
        if no is None:
            no = self.raiz
        for chave, filho in no.filhos.items():
            print(prefixo + chave + ("*" if filho.fim_palavra else ""))
            self.exibir(filho, prefixo + "  ")


    def salvar_em_disco(self, caminho_arquivo):
        """Salva a Trie em formato JSON."""
        estrutura = self._no_para_dict(self.raiz)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(estrutura, f, ensure_ascii=False, indent=2)
        print(f"Trie salva em {caminho_arquivo}")

    def carregar_de_disco(self, caminho_arquivo):
        """Reconstrói a Trie a partir de um arquivo JSON."""
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            estrutura = json.load(f)
        self.raiz = self._dict_para_no(estrutura)
        print(f"Trie carregada de {caminho_arquivo}")

    # ================================================================
    # FUNÇÕES RECURSIVAS AUXILIARES
    # ================================================================

    def _no_para_dict(self, no):
        """Converte o nó (recursivamente) em um dicionário JSON-serializável."""
        return {
            "fim_palavra": no.fim_palavra,
            "aparicoes": no.aparicoes,
            "filhos": {chave: self._no_para_dict(filho) for chave, filho in no.filhos.items()}
        }

    def _dict_para_no(self, dicionario):
        """Converte um dicionário de volta para um objeto NoCompacto."""
        no = NoCompacto()
        no.fim_palavra = dicionario["fim_palavra"]
        no.aparicoes = dicionario["aparicoes"]
        for chave, sub_no in dicionario["filhos"].items():
            no.filhos[chave] = self._dict_para_no(sub_no)
        return no