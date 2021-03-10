from flask import Flask,render_template,jsonify
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from jj import  jj, jj_dwjz
from zs import zs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zhouxi'
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

jj_codes = ['005969','004997','003834','005454','161725','570001','005827','001875', '968061']
zs_codes = ['1.000001','0.399001','0.399006']
zs_bh=[]
jj_bh=[]
jj_date=''

def jj_compare():
    global jj_bh,jj_date
    result = jj(jj_codes,jj_bh)
    jj_bh = result[0]
    jj_date = result[1]
    return result

def zs_compare():
    global zs_bh
    zs_bh = zs(zs_codes,zs_bh)
    return zs_bh

def jj_cz():
    global jj_date
    for j in jj_bh:
        j['bh'] = 0
    return [jj_bh,jj_date]

def zs_cz():
    for z in zs_bh:
        z['bh'] = 0
    return zs_bh

@app.route('/')
def hello_world():
    return render_template('index.html')

@socketio.on('zs_socket')
def handle_my_custom_event(data):
    print('received connection: ' + str(data))
    emit('zs',(zs_compare()))
    while True:
        socketio.sleep(3)
        emit('zs',(zs_compare()))
        #变化颜色重置
        socketio.sleep(1)
        emit('zs',(zs_cz()))

@socketio.on('jj_socket')
def send_jj(message):
    emit('jj',(jj_compare()))
    print('received connection: ' + str(message))
    while True:
        socketio.sleep(4)
        emit('jj',(jj_compare()))
        #变化颜色重置
        socketio.sleep(1)
        emit('jj',(jj_cz()))

if __name__ == '__main__':
    socketio.run(app,debug=True)