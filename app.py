import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import nbformat
from nbclient import NotebookClient

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<path:filename>")
def files(filename):
    return send_from_directory(BASE_DIR, filename)


@app.post("/search")
def search():
    data = request.get_json() or {}
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        notebook = nbformat.read("Patent_search_full_without_error.ipynb", as_version=4)

        # Make query available to the notebook
        notebook.cells.insert(
            0,
            nbformat.v4.new_code_cell(
                f"query = {query!r}"
            )
        )

        client = NotebookClient(
            notebook,
            timeout=600,
            kernel_name="python3"
        )

        client.execute()

        return jsonify({
            "message": "Notebook executed successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)