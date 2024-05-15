from flask import Flask, jsonify, send_file, request
import sqlite3
import base64
import os
import shutil

#Definerer variabler for videre bruk
app = Flask(__name__)
DATABASE = 'bilder.db'
IMAGE_SUBFOLDER = 'bilder'





#Funksjon for å hente alle bilder fra DB
def get_all_images():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    #Henter bilde og timestamp fra bilder tabellen
    cursor.execute("SELECT path, tidspunkt, dato FROM bilder ORDER BY tidspunkt DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows




def get_images_by_date_range(from_date, to_date):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    #Henter bilde og timestamp fra bilder tabellen innenfor et gitt tidsrom
    cursor.execute("SELECT path, tidspunkt, dato FROM bilder WHERE dato BETWEEN ? AND ? ORDER BY tidspunkt DESC", (from_date, to_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

def slett_alle_bilder():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS bilder')
    cursor.execute('CREATE TABLE bilder(id INTEGER PRIMARY KEY, path varchar(255), tidspunkt DATETIME, dato TEXT)')







#Henter bildedata fra hver rad i tabellen og returnerer de i image_data liste
@app.route('/all_images')
def all_images():
    images = get_all_images()
    image_data = []
    for image_row in images:
        image_path, tidspunkt, dato = image_row 
        image_path = os.path.join(IMAGE_SUBFOLDER, image_path)
        with open(image_path, 'rb') as f:
            image_binary = f.read()
        encoded_image = base64.b64encode(image_binary).decode('utf-8')
        image_data.append({"data": encoded_image, "tidspunkt": tidspunkt, "dato": dato, "path": image_path})
    return jsonify({"images": image_data})



@app.route('/filter_images')
def filter_images():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    images = get_images_by_date_range(from_date, to_date)
    image_data = []
    for image_row in images:
        image_path, tidspunkt, dato = image_row 
        image_path = os.path.join(IMAGE_SUBFOLDER, image_path)
        with open(image_path, 'rb') as f:
            image_binary = f.read()
        encoded_image = base64.b64encode(image_binary).decode('utf-8')
        image_data.append({"data": encoded_image, "tidspunkt": tidspunkt, "dato": dato, "path": image_path})
    return jsonify({"images": image_data})





def delete_image(image_path):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    filename = os.path.basename(image_path)
    cursor.execute("DELETE FROM bilder WHERE path = ?", (filename,))
    conn.commit()
    conn.close()
    
    abs_image_path = os.path.join(os.getcwd(), image_path)
    
    # Check if the file exists before attempting to remove it
    if os.path.exists(abs_image_path):
        os.remove(abs_image_path)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "File not found"})


def delete_all_images():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS bilder')
    cursor.execute('CREATE TABLE bilder(id INTEGER PRIMARY KEY, path varchar(255), tidspunkt DATETIME, dato TEXT)')
    conn.commit()
    conn.close()
    shutil.rmtree(IMAGE_SUBFOLDER)
    os.mkdir(IMAGE_SUBFOLDER)
    return jsonify({"success": True})



#Routes for slett bilde(r) funksjoner
@app.route('/delete_image', methods=['POST'])
def delete_image_route():
    image_path = request.form['image_path']
    return delete_image(image_path)

@app.route('/delete_all_images', methods=['POST'])
def delete_all_images_route():
    return delete_all_images()




#Kode som snakker med front-end
@app.route('/sss3000r.html')
def serve_html():
    return send_file('sss3000r.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
