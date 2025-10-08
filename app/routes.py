from flask import Blueprint, render_template, request
import math

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
  query = None
  results_on_page = None
  total_pages = None
  page = request.args.get("page", 1, type=int)
  per_page = 3 

  results = [
    {"title": "BBC News sobre economia", "snippet": "O mercado global..."},
    {"title": "BBC News sobre política", "snippet": "O governo anunciou..."},
    {"title": "BBC News sobre farmácia", "snippet": "O mercado global..."},
    {"title": "BBC News sobre saúde", "snippet": "O governo anunciou..."},
    {"title": "BBC News sobre festa", "snippet": "O mercado global..."},
    {"title": "BBC News sobre festival", "snippet": "O mercado global..."},
    {"title": "BBC News sobre guerra", "snippet": "O governo anunciou..."}
  ]

  if request.method == "POST":
    query = request.form.get("q")
    # results = search_controller.search(query)

  start = (page - 1) * per_page
  end = start + per_page
  results_on_page = results[start:end]
  total_pages = math.ceil(len(results) / per_page)

  return render_template(
    "index.html",
    query=query,
    results_on_page=results_on_page,
    total_pages=total_pages,
    page=page
  )

