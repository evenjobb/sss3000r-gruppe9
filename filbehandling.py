import os
from datetime import datetime
from time import localtime
from PIL import Image
import sqlite3 as lite
import sys

# hvis ansikt gjenkjennes, slett bilde som ble tatt med PiCamera
def slett_bilde():
    # sjekk om fil eksisterer, så slett
    # hvis bilde ikke finnes, print feilmelding
    if os.path.exists("bilde.jpg"):
        os.remove("bilde.jpg")
        print("Bilde slettet")
    else:
        print("Fil 'bilde.jpg' finnes ikke!")
    

# hvis ansikt ikke gjenkjennes, lagre bilde som ble tatt med PiCamera
# i mappen bilder. dette med videre visning av bilder i en webløsning
def lagre_bilde():
    # opprett filnavn med UNIX timestamp
    tid = str(datetime.now().timestamp())
    nyFilNavn = "bilder/" + tid + ".jpg"
    nyFilNavnUtenPath = tid + ".jpg"
    
    # sjekk om fil eksisterer, så flytt
    # hvis bilde ikke finnes, print feilmelding
    if os.path.exists('bilde.jpg'):

        # roterer bilde 180 grader
        bilde = Image.open('bilde.jpg')
        bilde = bilde.rotate(180)
        # viser bilde - kun for testing
        #bilde.show()
        # lagrer det roterte bilde
        bilde = bilde.save('rotert_bilde.jpg')
        
        # flytt bilde, endre filnavn
        os.replace('rotert_bilde.jpg', nyFilNavn)
        print("Bilde lagret")

        db_settinn(nyFilNavnUtenPath)
        print("Fil lagt til database")
    else:
        print("fil 'bilde.jpg' finnes ikke!")

    return nyFilNavn

# setter inn filnavn i database, med tidspunkt og dato.
def db_settinn(filnavn):
    dato = datetime.today().strftime('%Y-%m-%d')
    connection = lite.connect('bilder.db')
    # sql innsetting
    with connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO bilder (path, tidspunkt, dato) VALUES(?, datetime('now', 'localtime'), ?)",
                    (filnavn, dato,))
        connection.commit()
        
