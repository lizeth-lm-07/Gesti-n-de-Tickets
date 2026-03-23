from flask import Flask, render_template, request, redirect, url_for
from api_01 import Database
from database import init_db


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']
        print("Correo recibido:", username)
        print("Contraseña recibida:", password)

        db_instance = Database("tickets.db")
        user = db_instance.login(username, password)
        print("Usuario encontrado:", user)

        print("Datos del formulario:", request.form)

        if user:
            tipo_usuario = user[2]
            if tipo_usuario == 3:
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_usuario.html')


@app.route('/dashboard_admin')
def dashboard_admin():
    # Puedes crear dashboard_admin.html o reutilizar dashboard_usuario.html
    return render_template('dashboard_usuario.html')


@app.route('/crear_ticket')
def crear_ticket():
    return render_template('crear_ticket.html')


@app.route('/status')
def status():
    return render_template('status_ticket.html')


if __name__ == '__main__':
    init_db()  # Inicializa la base de datos y tablas al arrancar
    app.run(debug=True)