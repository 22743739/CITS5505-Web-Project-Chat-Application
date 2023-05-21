from setup import socketio
from flask_socketio import send, emit, join_room, leave_room


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('my_event')
def handle_my_custom_event(data):
    print('received message: ' + str(data))
    send('server side')
    emit('my response ', data)


@socketio.on('connect')
def handle_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def handle_disconect():
    print('Client disconnected')
