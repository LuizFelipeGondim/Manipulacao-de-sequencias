from flask import Blueprint, render_template, request, session
import math
from .controllers import SearchController

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
  controller = SearchController()
  per_page = 5
  page = request.args.get("page", 1, type=int)

  if request.method == "POST":
    query = request.form.get("q")
    results = controller.searchResults(query)

    session["query"] = query
    session["results"] = results

  else:
    if "results" in session:
      query = session.get("query")
      results = session.get("results")
    else:
      results = controller.searchResults(None)
      session["results"] = results

  # Paginacao
  start = (page - 1) * per_page
  end = start + per_page
  results_on_page = results[start:end]
  total_pages = math.ceil(len(results) / per_page)

  category_icons = {
    "tech": "img/tech.svg",
    "sports": "img/sports.svg",
    "business": "img/business.svg",
    "politics": "img/politics.svg",
    "entertainments": "img/entertainments.svg"
  }

  return render_template(
    "index.html",
    page=page,
    query=query,
    total_pages=total_pages,
    category_icons=category_icons,
    results_on_page=results_on_page
  )
