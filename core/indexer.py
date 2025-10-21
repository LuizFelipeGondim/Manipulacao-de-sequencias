from trie import CompactTrie
from utils import disk_exists

class InvertedIndex:
    def __init__(self):
        self.documents = []
        self.trie = CompactTrie()
        self.files_read = 0

        if disk_exists() == True:
            self.load_from_disk("../index_storage/disk.json")

    def __del__(self):
        if disk_exists() == False:
            self.save_to_disk("../index_storage/disk.json")      

    def add_file(self, content, document_name):
        self.documents.append(document_name)
        word_list = content.split()

        for word in word_list:
            self.trie.insert_word(word, document_name)

    def show_trie(self):
        self.trie.display()

    def search_word(self, word):
        self.trie.search_word(word)
    
    def save_to_disk(self, path):
        self.trie.save_to_disk(path)

    def load_from_disk(self, path):
        self.trie.load_from_disk(path)
