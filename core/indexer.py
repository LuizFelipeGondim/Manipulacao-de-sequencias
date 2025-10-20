from trie import TrieCompacta

class IndiceInvertido:
    def __init__(self):
        self.documentos = []
        self.trie = TrieCompacta()
        self.arquivos_lidos = 0

    def adicionarArquivo(self, conteudo, nome_documento):
    
        self.documentos.append(nome_documento)
        lista_palavras = conteudo.split()

        for palavra in lista_palavras:
            self.trie.inserirPalavra(palavra, nome_documento)
 

    def exibirDocumentos(self):
        print(self.documentos)
        self.trie.exibir()

    def pesquisarPalavra(self, palavra):
        self.trie.buscarPalavra(palavra)
    