from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    # palindrome()
    # arr_test = [40, 22, 35, 9, 19, 82]
    # merge_sort(arr_test)
    # print(arr_test)
    # sortArray()
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')


@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/addscripture')
def addscripture():
    pass
    return render_template('addscripture.html')

@app.route('/statement')
def statement():
    return render_template('statement.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)

