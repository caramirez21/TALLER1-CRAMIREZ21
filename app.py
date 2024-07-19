from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/lassie')
def mostrar_lassie():
    lassies = Perro.query.filter_by(nombre='Lassie').all()
    lassie_count = len(lassies)
    return render_template('cuidador.html', lassie_count=lassie_count, lassies=lassies, mario_perros=[])


@app.route('/mario')
def asignar_mario():
    mario = Cuidador.query.filter_by(nombre='Mario').first()
    if mario:
        mario_perros = Perro.query.filter(Perro.peso < 3).all()
        for perro in mario_perros:
            perro.id_cuidador = mario.id
        db.session.commit()
        return render_template('cuidador.html', lassie_count=0, lassies=[], mario_perros=mario_perros)
    else:
        return "Cuidador Mario no encontrado"


if __name__ == '__main__':
    app.run(debug=True)
