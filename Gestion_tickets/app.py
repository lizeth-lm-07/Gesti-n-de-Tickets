import os
import time

from flask import Flask, render_template, request, redirect, url_for, session
from api_01 import Database
from database import init_db
from ia_clasificador import clasificar_ticket
from werkzeug.utils import secure_filename

# CONFIG
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tickets.db")

app = Flask(__name__)
app.secret_key = 'inbi_secret_key_2024'

UPLOAD_FOLDER = os.path.join(base_dir, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def mapear_categoria(nombre):
    return {"Infraestructura":1,"Servicios":2,"Docencia":3,"Administrativo":4}.get(nombre,2)

def mapear_prioridad(nombre):
    return {"Baja":1,"Media":2,"Alta":3}.get(nombre,2)

# LOGIN
@app.route('/', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        db = Database("tickets.db")
        user = db.login(request.form['correo'], request.form['contrasena'])

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard_admin' if user[2]==3 else 'dashboard'))

        return render_template('login.html', error="Credenciales incorrectas")

    return render_template('login.html')

# DASHBOARD ADMIN
@app.route('/dashboard_admin')
def dashboard_admin():
    db = Database(db_path)
    tickets = db.obtener_todos_tickets()

    return render_template('dashboard_admin.html', tickets=tickets)

# CREAR TICKET
@app.route('/crear_ticket', methods=['GET','POST'])
def crear_ticket():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = Database(db_path)

    if request.method == 'POST':
        archivo = request.files.get('archivo')
        nombre_archivo = None

        if archivo and archivo.filename:
            filename = str(int(time.time())) + "_" + secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            nombre_archivo = filename

        resultado = clasificar_ticket(request.form['descripcion'])

        db.crear_ticket(
            request.form['titulo'],
            request.form['descripcion'],
            mapear_categoria(resultado.get("categoria")),
            mapear_prioridad(resultado.get("prioridad")),
            session['user_id'],
            nombre_archivo
        )

        return redirect(url_for('dashboard'))

    return render_template('crear_ticket.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)