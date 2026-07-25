from flask import Flask, render_template, request, send_file
from scanner import scan_website
from report import generate_report

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    url = ""

    if request.method == "POST":

        url = request.form["url"]

        try:
            result = scan_website(url)

        except Exception as e:

            result = {
                "error": str(e)
            }

    return render_template(
        "index.html",
        result=result,
        url=url
    )


@app.route("/download", methods=["POST"])
def download():

    url = request.form["url"]

    result = scan_website(url)

    filepath = generate_report(result)

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)