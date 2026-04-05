from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
socketio = SocketIO(app, cors_allowed_origins="*")

messages = []
online_users = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    global online_users
    online_users += 1
    emit('load_history', messages)
    socketio.emit('user_count', online_users)

@socketio.on('disconnect')
def on_disconnect():
    global online_users
    online_users = max(0, online_users - 1)
    socketio.emit('user_count', online_users)

@socketio.on('send_message')
def handle_message(data):
    messages.append(data)
    if len(messages) > 50:
        messages.pop(0)
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
