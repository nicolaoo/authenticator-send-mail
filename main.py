from flask import Flask, render_template, request, flash, redirect,url_for
from wtforms import Form, StringField,PasswordField, validators

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class RegistrationForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=40), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])

@app.route("/")
@app.route("/<name>")
def index(name=None):
    return render_template('index.html', name=name )
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            password = form.password.data

            flash('Registrazione avvenuta con successo!', 'success')
            return render_template('index.html', email=email, password=password )
        else:
            flash('Errore nella compilazione del form. Controlla i campi evidenziati.', 'danger')

    return render_template('login.html', form=form)