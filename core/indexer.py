from .trie import CompactTrie
from .utils import disk_exists, normalize
from pathlib import Path

class InvertedIndex:
    def __init__(self):
        self.documents = []
        self.trie = CompactTrie()
        self.files_read = 0

        if disk_exists() == True:
            self.load_from_disk("index_storage/disk.json")
        else:
            base_path = Path("data")
            for file in sorted(base_path.rglob("*.txt")):
                with open(file, "r") as txt_file:
                    content = txt_file.read()
                    content = normalize(content)
                    self.add_file(content, file.name)

    def __del__(self):
        if disk_exists() == False:
            self.save_to_disk("index_storage/disk.json")      

    def add_file(self, content, document_name):
        self.documents.append(document_name)
        word_list = content.split()

        for word in word_list:
            self.trie.insert_word(word, document_name)

    def search_word(self, word):
        return self.trie.search_word(word)
    
    def save_to_disk(self, path):
        self.trie.save_to_disk(path)

    def load_from_disk(self, path):
        self.trie.load_from_disk(path)
