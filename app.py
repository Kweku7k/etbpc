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

@app.route('/',methods=['GET','POST'])
def home():
    scripture = Scripture.query.order_by(Scripture.id.desc()).first()
    print(scripture)
    return render_template('index.html', scripture=scripture)


@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')



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

@app.route('/statement')
def statement():
    return render_template('statement.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)

