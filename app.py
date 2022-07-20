from flask import Flask, flash,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from forms import *
from datetime import datetime
import requests
import json

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


def payWithPaystack(email, amount, currency):
    if currency == 'GHS':
        data ={ "email": email, "amount": amount, "subaccount":'ACCT_jttrnvrmw7w2a4z', "callback_url":"https://etbpc.com/thanks", "channels":['card','bank', 'mobile_money'] }
    else:
        data ={ "email": email, "amount": amount, "subaccount":'ACCT_jttrnvrmw7w2a4z', "callback_url":"https://etbpc.com/thanks", "channels":['card','bank'] }
        
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        "Authorization": "Bearer sk_live_2cd142483915bea9a7602d4c6de8b546151fad6b",
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    thisdict = json.loads(response.text)
    print(thisdict)
    authorizationUrl = thisdict['data']['authorization_url']
    print(authorizationUrl)
    return authorizationUrl


@app.route('/donate', methods=['POST','GET'])
def donate():
    form = ConvertCurrency()
    if form.validate_on_submit():
        print("validated")
        amount = form.amount.data
        currency = form.currency.data
        email = form.email.data
        result = convertCurrency(currency, amount)
        print(result)
        result = json.loads(result)['result']
        print(result)
        rounded = int(round(result, 2)*100)
        print("rounded = " + str(rounded))
        # print("round")
        # print(round(result, 2))
        # roundedAmount = float(round(result, 2))
        # print("rounded amount " + str(roundedAmount))
        # print(roundedAmount * 100)
        authUrl = payWithPaystack(email, rounded, currency)
        print(authUrl)
        return redirect(authUrl)
        # return redirect('https://paystack.com/pay/mv94id5n1y')
    else:
        print(form.errors)
        # flash(f'There was a problem','danger')
    return render_template('paymentForm.html', form=form)
    # return redirect('https://flutterwave.com/donate/9xn5chvled9b')
    # return redirect('https://flutterwave.com/pay/etbpc?_gl=1%2a1f9j092%2a_ga%2aMTQ2NDIxMDAzMS4xNjU1NzU5NDU3%2a_ga_KQ9NSEMFCF%2aMTY1NjA2NzQxNy4zLjEuMTY1NjA2ODEyMy4w')

@app.route('/donated')
def donated():
    return render_template('donated.html')
    
@app.route('/thanks', methods=['GET', 'POST'])
def thanks():
    return render_template('thanks.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


def convertCurrency(currency, amount):
    url = "https://api.apilayer.com/currency_data/convert?to=GHS&from="+ currency +"&amount="+ amount 

    payload = {}
    headers= {
    # "apikey": "KggjPZDWQHGB8eHxmWefEkeH1JiKUogx"
    "apikey": "1hJTCcWfCNngk1XilsuU5wE6jBen6wtM"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    print(status_code)
    result = response.text
    return result

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

