// Responsável por fazer a manipulação do CSS ao alterar o switch de tema da página.

const checkbox = document.getElementById("switch-checkbox");

const black = "#16161D";
const lightBlack = "#2C2C2C";
const gray = "#9C98A6";
const lightGray = "#F0F0F7";
const lightShadow = "#cccccc";

const svgs = document.querySelectorAll(".switch-svg");
const title = document.querySelector(".main-title");
const search = document.querySelector(".search");
const resultMessages = document.querySelectorAll(".result-message");
const cards = document.querySelectorAll(".card-container");
const cardTitles = document.querySelectorAll(".card-title");
const paginationText = document.querySelector(".pagination-text");
const newsParagraphs = document.querySelectorAll(".news-paragraph");

function setDarkMode() {
    document.body.style.backgroundColor = black;
	title.style.color = lightGray;
    
    if (search && search.style) {
        search.style.backgroundColor = lightBlack;
        search.style.color = lightGray;
    }

    if (paginationText && paginationText.style) paginationText.style.color = lightGray;

	if (cardTitles && cardTitles.length) {
        cardTitles.forEach((item) => {
            item.style.color = lightGray;
        });
    } 

    if (newsParagraphs && newsParagraphs.length) {
        newsParagraphs.forEach((item) => {
            item.style.color = lightGray;
        });
    }

	resultMessages.forEach((item) => {
		item.style.color = lightGray;
	});

    cards.forEach((item) => {
        item.style.backgroundColor = lightBlack;
    });

    svgs.forEach((item) => {
        item.style.fill = gray;
    });

    localStorage.setItem("@dark-mode", "enabled")
}

function setLightMode() {
    document.body.style.backgroundColor = lightGray;
    title.style.color = black;
    
    if (search && search.style) {
        search.style.backgroundColor = "white";
        search.style.color = lightBlack;
    }

    if (paginationText && paginationText.style) paginationText.style.color = black;

	if (cardTitles && cardTitles.length) {
        cardTitles.forEach((item) => {
            item.style.color = black;
        });
    }

    if (newsParagraphs && newsParagraphs.length) {
        newsParagraphs.forEach((item) => {
            item.style.color = lightBlack;
        });
    }

	resultMessages.forEach((item) => {
		item.style.color = lightBlack;
	});

    cards.forEach((item) => {
        item.style.backgroundColor = "white";
    });

    svgs.forEach((item) => {
        item.style.fill = black;
    });

    localStorage.removeItem("@dark-mode");
}

checkbox.addEventListener("change", function() {
    if (checkbox.checked) {
        setDarkMode();
    } else {
        setLightMode();
    }
})

if (localStorage.getItem("@dark-mode") === "enabled") {
    checkbox.checked = true;
    setDarkMode();
}