from flask import Flask, render_template
import sqlite3
from database import init_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    init_db()        # crea la base de datos y tablas
    app.run(debug=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_usuario.html')


@app.route('/crear_ticket')
def crear_ticket():
    return render_template('crear_ticket.html')