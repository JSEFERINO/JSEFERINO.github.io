from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    estatura = db.Column(db.Float, nullable=False)
    programa = db.Column(db.String(80), nullable=False)
    semestre = db.Column(db.String(80), nullable=False)
    grupo_sanguineo = db.Column(db.String(10), nullable=False)
    residencia = db.Column(db.String(80), nullable=False)
    estrato = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        peso = request.form['peso']
        estatura = request.form['estatura']
        programa = request.form['programa']
        semestre = request.form['semestre']
        grupo_sanguineo = request.form['grupo_sanguineo']
        residencia = request.form['residencia']
        estrato = request.form['estrato']

        usuario = Usuario(nombre=nombre, edad=edad, peso=peso, estatura=estatura, programa=programa, semestre=semestre, grupo_sanguineo=grupo_sanguineo, residencia=residencia, estrato=estrato)
        db.session.add(usuario)
        db.session.commit()

    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/exportar_csv')
def exportar_csv():
    usuarios = Usuario.query.all()
    with open('usuarios.csv', 'w', newline='') as csvfile:
        fieldnames = ['nombre', 'edad', 'peso', 'estatura', 'programa', 'semestre', 'grupo_sanguineo', 'residencia', 'estrato']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for usuario in usuarios:
            writer.writerow({
                'nombre': usuario.nombre,
                'edad': usuario.edad,
                'peso': usuario.peso,
                'estatura': usuario.estatura,
                'programa': usuario.programa,
                'semestre': usuario.semestre,
                'grupo_sanguineo': usuario.grupo_sanguineo,
                'residencia': usuario.residencia,
                'estrato': usuario.estrato
            })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
