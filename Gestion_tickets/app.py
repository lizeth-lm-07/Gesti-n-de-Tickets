
import sqlite3
from database import init_db
import flask as Flask
from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__, template_folder='templates', static_folder='static')  


@app.route('/')
def login( ):

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