from flask import Flask, render_template, request, redirect, url_for, flash
from data import users, nazev_webu, popis, technologie, titulek_webu
from generator import generator

app = Flask(__name__)
app.secret_key = "tajny_klic"  


@app.route("/", methods=["GET", "POST"])
def home():
    email = request.args.get("email")
    return render_template(
        "index.htm",
        nazev_webu=nazev_webu,
        titulek_webu=titulek_webu,
        popis=popis,
        technologie_webu=technologie,
        email=email
    )


@app.route("/contacts")
def contacts():
    return render_template("contacts.htm", users=users)


@app.route("/scripty")
def javascript():
    return render_template("javascript.htm")


@app.route("/generator")
def generator_page():
    cislo = generator()
    return render_template("generator.html", cislo=cislo, nazev_webu=nazev_webu)


produkty = [
    {"id": 1, "nazev": "Notebook Dell", "cena": 15000, "popis": "Výkonný notebook pro práci"},
    {"id": 2, "nazev": "Myš Logitech", "cena": 500, "popis": "Bezdrátová myš s precizním ovládáním"},
    {"id": 3, "nazev": "Klávesnice Mechanická", "cena": 2000, "popis": "Mechanická herní klávesnice"},
    {"id": 4, "nazev": "Monitor 24\"", "cena": 4000, "popis": "Full HD monitor s IPS panelem"},
    {"id": 5, "nazev": "Telefon Samsung", "cena": 8000, "popis": "Chytrý telefon s Androidem"}
]


def vyhledej_produkty(hledany_vyraz):
    nalezene = []
    try:
        hledane_id = int(hledany_vyraz)
        nalezene.extend([p for p in produkty if p["id"] == hledane_id])
    except ValueError:
        pass

    hledany_vyraz_lower = hledany_vyraz.lower()
    nalezene.extend([
        p for p in produkty
        if hledany_vyraz_lower in p["nazev"].lower() or hledany_vyraz_lower in p["popis"].lower()
    ])
    return nalezene


@app.route("/eshop", methods=["GET", "POST"])
def eshop():
    produkty_k_zobrazeni = produkty
    hledany_vyraz = ""

    if request.method == "POST":
        if "hledat" in request.form:
            hledany_vyraz = request.form.get("q", "").strip()
            if hledany_vyraz:
                produkty_k_zobrazeni = vyhledej_produkty(hledany_vyraz)

        elif "pridat" in request.form:
            try:
                nova_cena = int(request.form.get("cena", 0))
                novy_nazev = request.form.get("nazev", "").strip()
                if novy_nazev and nova_cena > 0:
                    novy_produkt = {
                        "id": len(produkty) + 1,
                        "nazev": novy_nazev,
                        "cena": nova_cena,
                        "popis": request.form.get("popis", "").strip()
                    }
                    produkty.append(novy_produkt)
                    flash(f'Produkt "{novy_produkt["nazev"]}" byl přidán.', "success")
                else:
                    flash('Název a cena (větší než 0) jsou povinné.', "danger")
            except ValueError:
                flash('Cena musí být platné číslo.', "danger")

    return render_template(
        "eshop.htm",
        produkty=produkty_k_zobrazeni,
        hledany_vyraz=hledany_vyraz,
        nazev_webu=nazev_webu,
        titulek_webu="E-shop"
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "404.html",
        nazev_webu=nazev_webu,
        titulek_webu="Chyba 404"
    ), 404


if __name__ == "__main__":
    app.run(debug=True)
