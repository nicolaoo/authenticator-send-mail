from flask import Flask, render_template, request, flash, redirect,url_for
from wtforms import Form, StringField,PasswordField, validators
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class RegistrationForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=40), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])

# Configurazione di Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulazione di un database per utenti
users = {"nicolaheavy@gmail.com": {"password": "provalogin"}}

# Classe User per Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        if user_id in users:
            return User(user_id)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Form per la registrazione
class RegistrationForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=40), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])

# Form per il login
class LoginForm(Form):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

@app.route("/")
@app.route("/<name>")
def index(name=None):
    if current_user.is_authenticated:
        return render_template('index.html', name=name, email=current_user.id )
    else:
        return render_template('index.html', name=name, email=None )
        
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
            email = form.email.data
            password = form.password.data

            if email in users and users[email]['password'] == password:
                user = User(email)
                login_user(user)  # Login dell'utente
                flash('Login effettuato con successo!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Email o password errati. Riprova.', 'danger')

    return render_template('login.html', form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', email=current_user.id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)