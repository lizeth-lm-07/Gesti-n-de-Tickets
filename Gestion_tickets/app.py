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
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_usuario.html')





@app.route('/crear_ticket', methods=['GET', 'POST'])
def crear_ticket():

    if request.method == 'post':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        id_categoria = request.form['categoria']
        id_prioridad = request.form['prioridad']
        id_usuario = Database("tickets.db").login(request.form['correo'], request.form['contrasena'])[0]  # Obtener id_usuario del login

        db_instance = Database("tickets.db")
        db_instance.crear_ticket(titulo, descripcion, id_categoria, id_prioridad, id_usuario)

        ticket=db_instance.obtener_tickets(id_usuario=id_usuario)  # Verificar que el ticket se ha creado correctamente
        print("Ticket creado:", ticket)

        return redirect(url_for('dashboard'))


    
    return render_template('crear_ticket.html')


if __name__ == '__main__':
    init_db()  # Inicializa la base de datos y tablas al arrancar
    app.run(debug=True)