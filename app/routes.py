from flask import Blueprint, render_template, request, url_for
import math
from pathlib import Path
from .controllers import SearchController

main = Blueprint("main", __name__)

# Rota principal responsável por lidar com todas as requisições, página e envio de dados para o frontEnd
@main.route("/", methods=["GET", "POST"])
def index():
	controller = SearchController()
	per_page = 10
	page = request.args.get("page", 1, type=int)

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
	)

# Rota para exibir conteúdo completo de uma notícia, retorna erro caso a noticia nao exista.
@main.route("/news/<filename>", methods=["GET"])
def news(filename):
	try:
		file_path = Path("data") / filename
		query = request.args.get("q", "")
		page = request.args.get("page", 1, type=int)

		if not file_path.is_file():
			return render_template("news.html", error_msg="Arquivo não encontrado.")

		with open(file_path, "r", encoding="utf-8") as f:
			lines = f.readlines()

		if not lines:
			return render_template("news.html", error_msg="O arquivo está vazio.")

		title = lines[0].strip()
		paragraphs = [line.strip() for line in lines[1:] if line.strip()]

		if not paragraphs:
			return render_template("news.html", error_msg="Nenhum conteúdo disponível nesta notícia.")

		return render_template(
			"news.html", 
			title=title, 
			paragraphs=paragraphs, 
			filename=filename,
			page=page,
			query=query
		)

	except Exception as e:
		return render_template("news.html", error_msg="Ocorreu um erro interno ao processar a notícia.")

