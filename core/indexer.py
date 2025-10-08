from trie import TrieCompacta

class IndiceInvertido:
    def __init__(self):
        self.documentos = []
        self.trie = TrieCompacta()
        self.arquivos_lidos = 0

    def adicionarArquivo(self, conteudo):
        self.arquivos_lidos += 1
        self.documentos.append(self.arquivos_lidos)
        lista_palavras = conteudo.split()

        for palavra in lista_palavras:
            self.trie.inserirPalavra(palavra, self.arquivos_lidos)
        

    def exibirDocumentos(self):
        print(self.documentos)
        self.trie.exibir()

    def pesquisarPalavra(self, palavra):
        self.trie.buscarPalavra(palavra)
    