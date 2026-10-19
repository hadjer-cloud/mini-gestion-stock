from database import connecter_db

def ajouter_categorie(nom):
    con = connecter_db()
    cur = con.cursor()

    cur.execute(""" insert into categories (nom) VALUES (?)""", (nom,))
    
    con.commit()
    con.close()

def afficher_categories():
    con = connecter_db()
    cur = con.cursor()
    
    cur.execute(" select * from categories" )
    categories = cur.fetchall()
        
    con.close()
    return categories