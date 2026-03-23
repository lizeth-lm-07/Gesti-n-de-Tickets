import os

from flask import Flask, render_template, request, redirect, url_for, session
from api_01 import Database
from database import init_db



base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tickets.db")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'  # Replace with a secure random key
app.secret_key = 'your_secret_key'  # Needed for session management

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
            session['user_id'] = user[0]  # Store user ID in session
            tipo_usuario = user[2]
            if tipo_usuario == 3:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_usuario.html')



@app.route('/crear_ticket', methods=['GET', 'POST'])
def crear_ticket():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        id_categoria = request.form['categoria']
        id_prioridad = request.form['prioridad']
        id_usuario = session.get('user_id')  # Get user ID from session

        if id_usuario is None:
            return redirect(url_for('login_page'))  # Redirect to login if not logged in

        db_instance = Database(db_path)
        db_instance.crear_ticket(titulo, descripcion, id_categoria, id_prioridad, id_usuario)

        return redirect(url_for('dashboard'))


    
    return render_template('crear_ticket.html')


    
if __name__ == '__main__':
    init_db()  # Inicializa la base de datos y tablas al arrancar
    app.run(debug=True)