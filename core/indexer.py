from trie import TrieCompacta
from utils import existeDisco

class IndiceInvertido:
    def __init__(self):
        self.documentos = []
        self.trie = TrieCompacta()
        self.arquivos_lidos = 0

        if(existeDisco() == True):
            self.carregarDisco("../index_storage/disk.json")

    def __del__(self):
        if(existeDisco() == False):
            self.salvarDisco("../index_storage/disk.json")      

    def adicionarArquivo(self, conteudo, nome_documento):
    
        self.documentos.append(nome_documento)
        lista_palavras = conteudo.split()

        for palavra in lista_palavras:
            self.trie.inserirPalavra(palavra, nome_documento)
 

    def exibirTrie(self):
        self.trie.exibir()

    def pesquisarPalavra(self, palavra):
        self.trie.buscarPalavra(palavra)
    
    def salvarDisco(self, caminho):
        self.trie.salvar_em_disco(caminho)

    def carregarDisco(self, caminho):
        self.trie.carregar_de_disco(caminho)
