from database import connecter_db
from datetime import datetime

def ajouter_produits(nom, prix, quantite, categorie_id):
    con = connecter_db()
    cur = con.cursor()


    cur.execute(""" insert into produits (nom, prix, quantite, categorie_id) VALUES (?,?,?,?)""", (nom, prix, quantite, categorie_id))

    con.commit()
    con.close()


def afficher_produits():
    con = connecter_db()
    cur = con.cursor()

    res = cur.execute(""" SELECT produits.id, produits.nom, produits.prix, produits.quantite, categories.nom
    FROM produits JOIN categories ON produits.categorie_id = categories.id """)

    produits = res.fetchall()
    con.close()

    return produits

def modifier_produit(id_produit, nom, prix, quantite, categorie_id):
    con = connecter_db()
    cur = con.cursor()

    cur.execute("""
        UPDATE produits 
        SET nom = ?, prix = ?, quantite = ?, categorie_id = ?  
        WHERE id = ?
        """, (nom, prix, quantite, categorie_id, id_produit))

    con.commit()
    con.close()


def supprimer_produits(id_produit):
    con = connecter_db()
    cur = con.cursor()

    cur.execute("delete from produits where id = ?", (id_produit,))

    con.commit()
    con.close()

def entree_stock(id_produit, quantite):
    con = connecter_db()
    cur = con.cursor()

    #augmenter la quantité du produit 
    cur.execute("UPDATE produits SET quantite = quantite + ? where id = ?", (quantite, id_produit))

    # Enregistrer le mouvement
    cur.execute("""
        INSERT INTO mouvements
        (produit_id, type_mouvement, quantite, date_mouvement)
        VALUES (?, ?, ?, ?)
    """, (id_produit, "entree", quantite, datetime.now().isoformat(timespec="seconds")))

    con.commit()
    con.close()



def sortie_stock(id_produit, quantite):
    if quantite <= 0:
        raise ValueError("La quantité doit être positive")

    con = connecter_db()
    cur = con.cursor()

    try:
        # Vérifier le stock disponible
        cur.execute(
            "SELECT quantite FROM produits WHERE id = ?",
            (id_produit,)
        )
        resultat = cur.fetchone()

        if resultat is None:
            raise ValueError("Produit introuvable")

        if resultat[0] < quantite:
            raise ValueError("Stock insuffisant")

        # Diminuer la quantité
        cur.execute(
            "UPDATE produits SET quantite = quantite - ? WHERE id = ?",
            (quantite, id_produit)
        )

        # Enregistrer le mouvement
        cur.execute("""
            INSERT INTO mouvements
            (produit_id, type_mouvement, quantite, date_mouvement)
            VALUES (?, ?, ?, ?)
        """, (
            id_produit,
            "sortie",
            quantite,
            datetime.now().isoformat(timespec="seconds")
        ))

        con.commit()

    except Exception:
        con.rollback()
        raise

    finally:
        con.close()


def afficher_mouvements():
    con = connecter_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            mouvements.id,
            produits.nom,
            mouvements.type_mouvement,
            mouvements.quantite,
            mouvements.date_mouvement
        FROM mouvements
        JOIN produits
            ON mouvements.produit_id = produits.id
        ORDER BY mouvements.id DESC
    """)

    mouvements = cur.fetchall()
    con.close()

    return mouvements





