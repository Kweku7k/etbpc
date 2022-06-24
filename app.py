from flask import Flask, flash,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from forms import *
from datetime import datetime

app=Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'll91628bb0b13ce0c676d32e2vsba245'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'


class Scripture(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    link = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # author = db.Column(db.String)
    # image_file = db.Column(db.String(200), default='default.png')
    
    def __repr__(self):
        return f"Scripture('{self.id}', '{self.title}')"


class Update(db.Model):
    tablename = ['Update']

    id = db.Column(db.Integer, primary_key=True)
    field1 = db.Column(db.String)
    field2 = db.Column(db.String)
    field3 = db.Column(db.String)
    field4 = db.Column(db.String)
    date = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # author = db.Column(db.String)
    # image_file = db.Column(db.String(200), default='default.png')
    
    def __repr__(self):
        return f"Scripture('{self.id}', '{self.date}')"

@app.route('/',methods=['GET','POST'])
def home():
    scripture = Scripture.query.order_by(Scripture.id.desc()).first()
    update = Update.query.order_by(Update.id.desc()).first()
    print(scripture)
    print(update)
    return render_template('index.html', scripture=scripture, update=update)


@app.route('/donate')
def donate():
    # return redirect('https://paystack.com/pay/mv94id5n1y')
    # return redirect('https://flutterwave.com/donate/9xn5chvled9b')
    return redirect('https://flutterwave.com/pay/etbpc?_gl=1%2a1f9j092%2a_ga%2aMTQ2NDIxMDAzMS4xNjU1NzU5NDU3%2a_ga_KQ9NSEMFCF%2aMTY1NjA2NzQxNy4zLjEuMTY1NjA2ODEyMy4w')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/updates')
def updates():
    return render_template('updates.html')

@app.route('/allupdates')
def allupdates():
    updates = Update.query.all()
    return render_template('allupdates.html', updates=updates)

@app.route('/addscripture', methods=['GET','POST'])
def addscripture():
    form = ScriptureForm()
    if form.validate_on_submit():
        newScripture = Scripture(title=form.title.data, content=form.content.data, link=form.link.data)
        db.session.add(newScripture)
        db.session.commit()
        flash(f'New Scripture Updated.', 'success')
        return redirect(url_for('home'))
    return render_template('addscripture.html', form=form)

@app.route('/addupdate', methods=['GET','POST'])
def addupdate():
    form = UpdateForm()
    if form.validate_on_submit():
        newUpdate = Update(field1=form.field1.data, date=form.date.data, field2=form.field2.data, field3=form.field3.data, field4=form.field4.data)
        db.session.add(newUpdate)
        db.session.commit()
        flash(f'New update successful.', 'success')
        return redirect(url_for('home'))
    return render_template('addupdate.html', form=form)

@app.route('/statement')
def statement():
    return render_template('statement.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)

