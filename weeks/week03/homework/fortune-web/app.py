"""Flask front-end for the 算命 fortune-teller.

GET  /        → the input form
POST /fortune → build a profile, run every registered reading, render results

The web layer stays thin: all the first-class-function machinery lives in the
``fortune`` package. This file only validates input and renders.
"""

from __future__ import annotations

from flask import Flask, render_template, request

from fortune import FortuneTeller, ProfileError, build_profile

app = Flask(__name__)

# One teller instance for the process — its __call__ keeps a history (§1.5).
teller = FortuneTeller()


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/fortune")
def fortune_view() -> str:
    name = request.form.get("name", "")
    birthday = request.form.get("birthday", "")
    try:
        profile = build_profile(name=name, birthday=birthday)
    except ProfileError as exc:
        # User-friendly message on the form; never leak a stack trace.
        return render_template("index.html", error=str(exc), name=name, birthday=birthday)

    results = teller(profile)
    return render_template(
        "index.html",
        name=name,
        birthday=birthday,
        results=results,
        consultations=teller.consultations,
    )


if __name__ == "__main__":
    app.run(debug=True)
