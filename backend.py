from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil.relativedelta import relativedelta



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:\\python\\FlaskSQLAlchemy\\app.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


class dob(db.Model):
    id = db.Column('dob_id', db.Integer, primary_key = True)
    dob = db.Column(db.String(100))
    age = db.Column(db.String(100))

    def __init__(self, dob, age):
        self.dob = dob
        self.age = age

@app.route('/')
def show_all():
   return render_template('frontend.html', dob = dob.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['dob']:
         flash('Please enter all the fields', 'error')
      else:
        birth = request.form['dob']
        birthDate = datetime.strptime(birth, "%Y-%m-%d").date()
        current = datetime.date(datetime.now())
        rdelta = relativedelta(current, birthDate)
        result = str(rdelta.years) + " years "+ str(rdelta.months) + " months "+ str(rdelta.days) + " days"
        dobd = dob(request.form['dob'],result)
        db.session.add(dobd)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('show_all'))
   return render_template('addition.html')

@app.route('/delete')
def delete():
   dobd = dob.query.all()
   for Id in dobd:
      db.session.delete(Id)
   db.session.commit()
   return render_template('frontend.html', dob = dob.query.all() )

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)