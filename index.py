from flask import Flask, redirect, jsonify
from juggernaut import Juggernaut
from redis import Redis

app = Flask(__name__)
app.debug = True

db = Redis()
jug = Juggernaut()


@app.route('/')
def hello():
    return redirect('/static/index.html')


@app.route('/settext/<string:in_text>', methods=['POST'])
def settext(in_text):
    if(not db.get('text')):
        db.set('text', '')
    db.set('text', db.get('text').decode("utf8") + "," + in_text)
    res = db.get('text')
    result = {'result': res}
    jug.publish('settext', result)
    return jsonify(result)


@app.route('/gettext/', methods=['POST'])
def gettext():
    res = db.get('text')
    result = {'result': res}
    jug.publish('settext', result)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
