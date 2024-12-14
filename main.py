from flask import Flask, render_template, request, flash, redirect,url_for
from wtforms import Form, StringField,PasswordField, validators
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurazione Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nicolaguarise00@gmail.com'  # Cambia con il tuo indirizzo email
app.config['MAIL_PASSWORD'] = 'zyrhvorphptgmqic'  # App password generata da Google
app.config['MAIL_DEFAULT_SENDER'] = 'nicolaguarise00@gmail.com'  # Mittente predefinito
mail = Mail(app)

# Configurazione di Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
emails = ["example1@gmail.com", "example2@gmail.com"]


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
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=6, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=40), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])

# Form per il login
class LoginForm(Form):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

@app.route("/")
def index():
    if current_user.is_authenticated:
        name = users.get(current_user.id, {}).get('name', 'utente')
        return render_template('index.html', name=name, email=current_user.id )
    else:
        return render_template('index.html', name=None, email=None )
        
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        if email in users:
            # Passa url_for('login') al template per il link
            flash(f"L'email è già registrata. Prova a fare il <a class='text-white font-bold text-sm' href='{url_for('login')}'>login</a>.", 'danger')
        else:
            users[email] = {"password": password, "name": name}
            flash(f"Registrazione avvenuta con successo! Benvenuto, "+name+".", 'success')

            user = User(email)
            login_user(user)
  
            return redirect(url_for('dashboard'))

    return render_template('register.html', form=form)


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

@app.route("/send-email", methods=['GET', 'POST'])
def sender():
    feedback_message = None
    feedback_class = "text-red-500"

    if request.method == 'POST':
        recipient_email = request.form.get("recipient_email")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not recipient_email or not subject or not body:
            feedback_message = "Tutti i campi sono obbligatori."
        else:
            try:
                recipients = [email.strip() for email in recipient_email.split(",")]
                msg = Message(subject=subject,
                              sender="nicolaguarise00@gmail.com",  # Specifica il mittente
                              recipients=recipients,
                              body=body)
                mail.send(msg)
                feedback_message = "Email inviata con successo!"
                feedback_class = "text-green-500"
            except Exception as e:
                feedback_message = f"Errore nell'invio: {str(e)}"

    return render_template('send-email.html', feedback_class=feedback_class, feedback_message=feedback_message, emails=emails)


@app.route("/dashboard")
@login_required
def dashboard():
    name = users.get(current_user.id, {}).get('name', 'utente')
    return render_template('dashboard.html', name=name, email=current_user.id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)