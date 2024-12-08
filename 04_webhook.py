from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Route für die Eingabeseite
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Daten aus dem Formular abrufen
        siemens_url = request.form.get("siemens_url")
        bosch_url = request.form.get("bosch_url")
        api_token = request.form.get("api_token")
        username = request.form.get("username")

        # Daten speichern
        data = {
            "Category": ["Project URL", "API Token", "Username"],
            "Siemens": [siemens_url, api_token, username],
            "Bosch": [bosch_url, "", ""]
        }
        df = pd.DataFrame(data)
        df.to_csv("./data/project_data.csv", index=False)

        return redirect(url_for("success"))

    return render_template("index.html")


# Erfolgsseite nach Abspeichern der Daten
@app.route("/success")
def success():
    return "<h1>Data saved successfully!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
