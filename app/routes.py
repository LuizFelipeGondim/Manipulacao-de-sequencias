from flask import Blueprint, render_template, request, url_for
import math
from .controllers import SearchController

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
	controller = SearchController()
	per_page = 10
	page = request.args.get("page", 1, type=int)
	filename = ""

	results = []
	error_msg = None

	if request.method == "POST":
		query = request.form.get("q", "").strip()
		page = 1
	else:
		query = request.args.get("q", "").strip()

	if query:
		response = controller.searchResults(query)
		results = response.get("results", [])
		error_msg = response.get("error")
		filename = response.get("filename")

	# Paginação
	start = (page - 1) * per_page
	end = start + per_page
	results_on_page = results[start:end] if results else []
	total_pages = math.ceil(len(results) / per_page) if results else 0

	category_icons = {
		"tech": "img/tech.svg",
		"sport": "img/sport.svg",
		"business": "img/business.svg",
		"politics": "img/politics.svg",
		"entertainment": "img/entertainment.svg"
	}

	return render_template(
		"index.html",
		page=page,
		query=query,
		total_pages=total_pages,
		category_icons=category_icons,
		results_on_page=results_on_page,
		error_msg=error_msg,
		filename=filename
	)
