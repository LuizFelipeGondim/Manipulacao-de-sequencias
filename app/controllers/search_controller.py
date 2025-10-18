class SearchController:
  def __init__(self):
    self.results = []

  def searchResults(self, query):
    if not query:
      self.results = [{"title": "BBC News sobre festival", "snippet": "O mercado global...", "category": "tech"}]
      return self.results

    self.results = [
      {"title": "BBC News sobre economia", "snippet": "O mercado global...", "category": "tech"},
      {"title": "BBC News sobre política", "snippet": "O governo anunciou...", "category": "business"},
      {"title": "BBC News sobre farmácia", "snippet": "O mercado global...", "category": "entertainments"},
      {"title": "BBC News sobre saúde", "snippet": "O governo anunciou...", "category": "politics"},
      {"title": "BBC News sobre festa", "snippet": "O mercado global...", "category": "sports"},
      {"title": "BBC News sobre festival", "snippet": "O mercado global...", "category": "tech"},
      {"title": "BBC News sobre saúde", "snippet": "O governo anunciou...", "category": "politics"},
      {"title": "BBC News sobre festa", "snippet": "O mercado global...", "category": "sports"},
      {"title": "BBC News sobre festival", "snippet": "O mercado global...", "category": "tech"},
      {"title": "BBC News sobre guerra", "snippet": "O governo anunciou...", "category": "sports"}
    ]

    return self.results
  