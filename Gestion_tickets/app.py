import os

from flask import Flask, render_template, request, redirect, url_for, session
from api_01 import Database
from database import init_db
from ia_clasificador import clasificar_ticket

def mapear_categoria(nombre):
    mapa = {
        "Infraestructura": 1,
        "Servicios": 2,
        "Docencia": 3,
        "Administrativo": 4
    }
    return mapa.get(nombre, 2)

def mapear_prioridad(nombre):
    mapa = {
        "Baja": 1,
        "Media": 2,
        "Alta": 3
    }
    return mapa.get(nombre, 2)


base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tickets.db")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'inbi_secret_key_2024'

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['correo']
        password = request.form['contrasena']
        print("Correo:", username)
        print("Password:", password)

        db_instance = Database("tickets.db")
        user = db_instance.login(username, password)
        print("User:", user)

        if user:
            session['user_id'] = user[0]
            session['nombre'] = user[1]
            tipo_usuario = user[2]
            print("Tipo:", tipo_usuario)
            if tipo_usuario == 3:
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    id_usuario = session.get('user_id')

    if id_usuario is None:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)
    user = db_instance.obtener_usuario_por_id(id_usuario)

    # user = (id_usuario, nombre, correo, id_rol)
    nombre = user[1]

    return render_template('dashboard_usuario.html', nombre=nombre)

@app.route('/dashboard_admin')
def dashboard_admin():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)
    tickets = db_instance.obtener_todos_tickets()
    
    pendiente  = sum(1 for t in tickets if t[4] == 'Pendiente')
    en_proceso = sum(1 for t in tickets if t[4] == 'En proceso')
    resuelto   = sum(1 for t in tickets if t[4] == 'Resuelto')

    print("Tickets:", tickets)
    print("Pendiente:", pendiente)
    print("En proceso:", en_proceso)
    print("Resuelto:", resuelto)

    return render_template('dashboard_admin.html', 
                           tickets=tickets,
                           pendiente=pendiente,
                           en_proceso=en_proceso,
                           resuelto=resuelto)

@app.route('/crear_ticket', methods=['GET', 'POST'])
def crear_ticket():
    print("Método recibido:", request.method)
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        id_usuario = session['user_id']

        # 🔥 IA aquí
        resultado = clasificar_ticket(descripcion)

        categoria_texto = resultado.get("categoria", "Servicios")
        prioridad_texto = resultado.get("prioridad", "Media")

        id_categoria = mapear_categoria(categoria_texto)
        id_prioridad = mapear_prioridad(prioridad_texto)

        db_instance.crear_ticket(
            titulo,
            descripcion,
            id_categoria,
            id_prioridad,
            id_usuario,
            None
        )

        return redirect(url_for('dashboard'))

    categorias = db_instance.obtener_categorias()
    prioridades = db_instance.obtener_prioridades()

    return render_template(
        'crear_ticket.html',
        categorias=categorias,
        prioridades=prioridades
    )

@app.route('/status')
def status():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    db_instance = Database(db_path)
    tickets = db_instance.obtener_tickets_usuario(session['user_id'])
    return render_template('status_ticket.html', tickets=tickets)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        tipo = request.form['tipo']

        db_instance = Database(db_path)

        # Verificar si el usuario ya existe
        existe = db_instance.buscar_usuario(correo)

        if existe:
            return render_template('registro.html', error="El correo ya ya está registrado")

        # Registrar usuario
        db_instance.registrar_usuario(nombre, correo, contrasena, tipo)

        return redirect(url_for('login_page'))

    return render_template('registro.html')


@app.route('/gestion_tickets')
def gestion_tickets():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)
    tickets = db_instance.obtener_todos_tickets()

    # Filtros
    filtro_estado    = request.args.get('estado', '')
    filtro_prioridad = request.args.get('prioridad', '')
    filtro_categoria = request.args.get('categoria', '')

    if filtro_estado:
        tickets = [t for t in tickets if t[4] == filtro_estado]
    if filtro_prioridad:
        tickets = [t for t in tickets if t[3] == filtro_prioridad]
    if filtro_categoria:
        tickets = [t for t in tickets if t[2] == filtro_categoria]

    categorias  = db_instance.obtener_categorias()
    prioridades = db_instance.obtener_prioridades()

    return render_template('gestion_tickets.html',
                           tickets=tickets,
                           categorias=categorias,
                           prioridades=prioridades,
                           filtro_estado=filtro_estado,
                           filtro_prioridad=filtro_prioridad,
                           filtro_categoria=filtro_categoria)


@app.route('/detalle_ticket/<int:id_ticket>', methods=['GET', 'POST'])
def detalle_ticket(id_ticket):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)

    if request.method == 'POST':
        nuevo_estado = int(request.form['id_estado'])
        comentario   = request.form.get('comentario_admin', '')
        db_instance.actualizar_estado_ticket(id_ticket, nuevo_estado, comentario)
        return redirect(url_for('gestion_tickets'))  # ← adentro del if POST

    ticket = db_instance.obtener_ticket_detalle(id_ticket)
    estados = db_instance.obtener_estados()
    return render_template('detalle_ticket.html', ticket=ticket, estados=estados)

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html')


@app.route('/responsables', methods=['GET', 'POST'])
def responsables():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)

    if request.method == 'POST':
        cargo          = request.form['cargo']
        id_departamento = int(request.form['id_departamento'])
        correo         = request.form['correo']
        telefono       = request.form['telefono']
        db_instance.agregar_responsable(cargo, id_departamento, correo, telefono)
        return redirect(url_for('responsables'))

    responsables  = db_instance.obtener_responsables()
    departamentos = db_instance.obtener_departamentos()
    cargos = [
        'Jefe de Mantenimiento', 'Técnico de Soporte',
        'Jefe de Servicios', 'Coordinador de Servicios',
        'Coordinador Académico', 'Jefe de Área Académica',
        'Director Administrativo', 'Asistente Administrativo'
    ]
    return render_template('responsables.html',
                           responsables=responsables,
                           departamentos=departamentos,
                           cargos=cargos)


@app.route('/editar_responsable/<int:id_responsable>', methods=['GET', 'POST'])
def editar_responsable(id_responsable):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_instance = Database(db_path)

    if request.method == 'POST':
        cargo           = request.form['cargo']
        id_departamento = int(request.form['id_departamento'])
        correo          = request.form['correo']
        telefono        = request.form['telefono']
        db_instance.editar_responsable(id_responsable, cargo, id_departamento, correo, telefono)
        return redirect(url_for('responsables'))

    responsable   = db_instance.obtener_responsable_por_id(id_responsable)
    departamentos = db_instance.obtener_departamentos()
    cargos = [
        'Jefe de Mantenimiento', 'Técnico de Soporte',
        'Jefe de Servicios', 'Coordinador de Servicios',
        'Coordinador Académico', 'Jefe de Área Académica',
        'Director Administrativo', 'Asistente Administrativo'
    ]
    return render_template('editar_responsable.html',
                           responsable=responsable,
                           departamentos=departamentos,
                           cargos=cargos)

@app.route('/eliminar_responsable/<int:id_responsable>')
def eliminar_responsable(id_responsable):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    db_instance = Database(db_path)
    db_instance.eliminar_responsable(id_responsable)
    return redirect(url_for('responsables'))
    
if __name__ == '__main__':
    init_db()  # Inicializa la base de datos y tablas al arrancar
    app.run(debug=True)