import flask as Flask
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, template_folder='templates', static_folder='static')  


@app.route('/')
def login( ):

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
