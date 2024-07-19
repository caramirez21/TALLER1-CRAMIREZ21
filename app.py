from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)


class Usuario:
    def __init__(self, id, username, password, es_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin


usuarios = [
    Usuario(1, 'carlos', 'abc123', es_admin=False),
    Usuario(2, 'roberto', 'def456', es_admin=False),
    Usuario(3, 'admin', 'adminpass', es_admin=True),
]


class Cuidador(db.Model):
    __tablename__ = 'cuidadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))


class Perro(db.Model):
    __tablename__ = 'perros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    raza = db.Column(db.String(100))
    edad = db.Column(db.Integer)
    peso = db.Column(db.Float)
    id_cuidador = db.Column(db.Integer, db.ForeignKey('cuidadores.id'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in usuarios if u.username == username and u.password == password), None)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['es_admin'] = user.es_admin
            return redirect(url_for('index'))
        else:
            return 'Nombre de usuario o contraseña incorrectos', 401
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('es_admin', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'username' in session:
        return f"Hola, {session['username']}!"
    return redirect(url_for('login'))


@app.route('/perros')
def ver_perros():
    if 'username' in session:
        if session.get('es_admin'):
            perros = Perro.query.all()
            return render_template('perros.html', perros=perros)
        else:
            return f"Hola, {session['username']}! No tienes acceso a esta página."
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
