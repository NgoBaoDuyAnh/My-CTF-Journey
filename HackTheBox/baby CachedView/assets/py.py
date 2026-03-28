from flask import Flask,render_template,redirect

app = Flask(__name__)
@app.route('/')
def default():
    #return redirect('http://127.0.0.1/flag')
    return "",302,{"Location":"http://127.0.0.1/flag"}

@app.route('/index.html')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000)