import sqlite3
def connecter_db(): #ouvre la connextion a la base 
    con = sqlite3.connect("stock.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con


def creer_tables(): #crée les tables si elles n'existent pas
    con = connecter_db()
    cur = con.cursor()


    cur.execute("CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY, nom TEXT NOT NULL)")

    cur.execute("CREATE TABLE IF NOT EXISTS produits(id INTEGER PRIMARY KEY, nom TEXT NOT NULL, prix REAL, quantite INTEGER, categorie_id INTEGER, FOREIGN KEY (categorie_id) REFERENCES categories(id))")

    cur.execute("""CREATE TABLE IF NOT EXISTS mouvements(id INTEGER PRIMARY KEY, produit_id INTEGER NOT NULL, type_mouvement TEXT NOT NULL, quantite INTEGER NOT NULL, date_mouvement TEXT NOT NULL, FOREIGN KEY(produit_id) REFERENCES produits(id) )""")
    
    con.commit()
    con.close() #ferme la connextion apres la creation 

if __name__ == "__main__": #exécute la création des tables quand tu lances directement ce fichier.
    creer_tables() 
    
    
   



