from datetime import datetime
from sqlite3.dbapi2 import DatabaseError

from flask import *
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'safa'

db = SQLAlchemy(app)

# accout table


class Account(db.Model):
    costumer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

# Order detail table


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    costumer_id = db.Column(db.Integer, db.ForeignKey('account.costumer_id'))
    phone = db.Column(db.String(50))
    bottle = db.Column(db.String(50))
    flavor = db.Column(db.String(50))
    date_ordered = db.Column(db.DateTime, default=datetime.now)
    ammount = db.Column(db.String(50))
# item information table


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    scent = db.Column(db.String(50))
    bottle = db.Column(db.String(50))
    background = db.Column(db.String(50))

@app.route('/')
def home():
    if 'email' in session:
        email = session['email']
    items = Item.query.all()
    return render_template('Main page.html', items=items, email=email )



# dynamic route to a template


@app.route('/scent/<int:id>')
def scent(id):
    # this will use the id parameter to get the right data from the database and send it to the temnplate
    result = Item.query.filter_by(item_id=id).first()
    return render_template('Scent.html' , result = result)

@app.route('/add', methods=['POST','GET'])
def order():
    if request.method == 'POST':
        ammount = request.form.get('ammount')
        bottle = request.form.get('bottle')
        contact = request.form.get('contact')
        flavor = request.form.get('flavor')
        new_order = Order(ammount=ammount, bottle=bottle, phone=contact, flavor=flavor)
        db.session.add(new_order)
        db.session.commit()
    return redirect('/end')




@app.route('/register', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if all([name, email, password1, password2]):
            if password1 == password2:
                a = Account()
                a.name = name
                a.email = email
                a.password = generate_password_hash(password1)
                db.session.add(a)
                db.session.commit()
                session['email'] = request.form['email']
                return redirect('/') 
            else:
                flash('Passwords are not the same')
        else:
            flash('information is not complete')
    return render_template('Sign_up_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if all([email, password]):
            a = Account.query.filter(Account.email == email).first()
            if a:
                if check_password_hash(a.password, password):
                    session['account_password'] = a.password
                    session['email'] = request.form['email']
                    return redirect('/')
                else:
                    flash('Wrong password')
            else:
                flash('Account does not exist')
        else:
            flash('Information is not complete')
    return render_template('Sign_in_page.html')


@app.route('/end')
def end():
    return render_template('end.html')

@app.route('/in')
def get():
    return render_template('Sign_in_page.html')

@app.route('/logout')
def logout():
   # remove the email from the session if it is there
   session.pop('email', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
