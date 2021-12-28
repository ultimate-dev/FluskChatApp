from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '123456'
socketio = SocketIO(app)
CORS(app)


@app.route("/login", methods=["GET"])
def login():
    return render_template('login.html')


@app.route("/", methods=["GET"])
def chat():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    print("Bir Kullanıcı Bağlandı")


@socketio.on('disconnect')
def disconnect():
    print("Bir Kullanıcı Ayrıldı")


users = []
messages = []


@socketio.on('set_user')
def set_user(user):
    if(users.count(user) == 0):
        users.append(user)
    emit('users', {"users": users, "messages": messages}, broadcast=True)


@socketio.on('remove_user')
def remove_user(user):
    users = users.pop(users.index(user))
    emit('users', {"users": users, "messages": messages}, broadcast=True)


@socketio.on('send_message')
def send_message(message):
    messages.append(message)
    emit('messages', {"messages": messages}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="192.168.43.185", port=8080, debug=True)
