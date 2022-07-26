import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__,template_folder='.')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.secret_key = "supersecret"
db = SQLAlchemy(app)


migrate = Migrate(app,db)

class customers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    billing = db.Column(db.String(30), unique = False, nullable = False)
    info = db.Column(db.String(25), unique = False, nullable = False)

    def __repr__(self):
        return f"Id : {self.id}, Billing : {self.billing}"

    def __init__(self, id, billing, info):
        self.id = id
        self.billing = billing
        self.info = info


@app.route('/')
def display():  
    return render_template('display.html', customers = customers.query.all())
    

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['id'] or not request.form['billing'] or not request.form['id']:
         flash('Please enter all the fields', 'error')
      else:
         customer = customers(request.form['id'], request.form['billing'],
            request.form['info'])
         
         db.session.add(customer)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('display'))
   return render_template('new.html')

if __name__ == "__main__":
    app.run()