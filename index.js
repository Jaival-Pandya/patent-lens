const language = document.getElementById("language");
const otherLanguage = document.getElementById("otherLanguage");
const searchForm = document.getElementById("searchForm");
const resultsContainer = document.getElementById("resultsContainer");

language.addEventListener("change", function () {
	if (this.value === "other") {
		otherLanguage.hidden = false;
		otherLanguage.required = true;
	} else {
		otherLanguage.hidden = true;
		otherLanguage.required = false;
		otherLanguage.value = "";
	}
});

searchForm.addEventListener("submit", async function (event) {
	event.preventDefault();
	resultsContainer.textContent = "Searching...";

	const formData = new FormData(searchForm);
	const payload = {
		query: formData.get("query"),
		language: formData.get("language"),
		otherLanguage: formData.get("otherLanguage")
	};

	try {
		const response = await fetch("/search", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(payload)
		});

		const data = await response.json();
		if (!response.ok) {
			throw new Error(data.error || "Search failed.");
		}

		resultsContainer.textContent = data.summary;
	} catch (error) {
		resultsContainer.textContent = error.message;
	}
});