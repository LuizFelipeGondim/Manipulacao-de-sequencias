class NoCompacto:
    def __init__(self):
        self.filhos={}
        self.aparicoes={}

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

