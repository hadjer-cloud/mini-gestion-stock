from flask import Flask, render_template, request, redirect, url_for, flash
from produits import ajouter_produits, afficher_produits, modifier_produit, supprimer_produits, entree_stock, sortie_stock, afficher_mouvements
from categories import afficher_categories, ajouter_categorie
from database import creer_tables

app = Flask(__name__)

creer_tables()

app.secret_key = "cle-secrete-dev"

@app.route("/")  #indique que cette fonction répond à la page d’accueil.
def accueil():
    produits = afficher_produits() #récupère les produits enregistrés dans SQLite.
    categories = afficher_categories()
    return render_template("index.html", 
                           produits=produits,
                           categories = categories) #transmet les données au fichier HTML.



@app.route("/ajouter_categorie", methods=["POST"])
def ajouter_categorie_route():
    nom = request.form["nom"].strip()

    if nom:
        ajouter_categorie(nom)
        flash("Catégorie ajoutée avec succès.")
    else:
        flash("Veuillez saisir un nom de catégorie.")

    return redirect(url_for("accueil"))



@app.route("/ajouter", methods=["POST"])
def ajouter():
    nom = request.form["nom"]
    prix = float(request.form["prix"])
    quantite = int(request.form["quantite"])
    categorie_id = int(request.form["categorie_id"])
    ajouter_produits(nom, prix, quantite, categorie_id)
    return redirect(url_for("accueil"))


@app.route("/modifier/<int:id_produit>", methods=["GET", "POST"])
def modifier(id_produit):
    categories = afficher_categories()

    if request.method == "POST":
        nom = request.form["nom"]
        prix = float(request.form["prix"])
        quantite = int(request.form["quantite"])
        categorie_id = int(request.form["categorie_id"])

        modifier_produit(
            id_produit, nom, prix, quantite, categorie_id
        ) 
        return redirect(url_for("accueil"))
    
    produits = afficher_produits()

    produit = next(
        (p for p in produits if p[0] == id_produit),
        None
    )
    if produit is None:
        return "Produit introuvable", 404
    return render_template(
        "modifier.html",
        produit=produit,
        categories=categories
    )


@app.route("/supprimer/<int:id_produit>", methods=["POST"])
def supprimer(id_produit):
    if request.method == "POST":
        supprimer_produits(id_produit)
    return redirect(url_for("accueil"))




@app.route("/entree_stock", methods=["POST"])
def entree():
    id_produit = int(request.form["id_produit"])
    quantite = int(request.form["quantite"])

    try:
        entree_stock(id_produit, quantite)
        flash("Entrée de stock enregistrée avec succès.")
    except ValueError as erreur:
        flash(str(erreur))

    return redirect(url_for("accueil"))




@app.route("/sortie_stock", methods=["POST"])
def sortie():
    id_produit = int(request.form["id_produit"])
    quantite = int(request.form["quantite"])

    try:
        sortie_stock(id_produit, quantite)
        flash("Sortie de stock enregistrée avec succès.")
    except ValueError as erreur:
        flash(str(erreur))

    return redirect(url_for("accueil"))



@app.route("/historique")
def historique():
    mouvements = afficher_mouvements()
    return render_template(
        "historique.html",
        mouvements=mouvements
    )

        

if __name__ == "__main__":
    app.run(debug=True)


