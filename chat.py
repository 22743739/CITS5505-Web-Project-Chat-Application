from setup import socketio
from flask import jsonify
from flask_socketio import send, emit, join_room, leave_room
from handler import get_chat_room_id, get_chat_history, create_chat_message


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('connect')
def handle_connect():
    emit('message', {'type': 'connected', 'data': 'Connected'})


@socketio.on('disconnect')
def handle_disconect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):
    sender = int(data['sender'])
    receiver = int(data['receiver'])
    roomId = get_chat_room_id(sender, receiver)
    join_room(roomId)
    emit('message', {'type': 'Joined', 'roomId': roomId})
    chat_history = get_chat_history(sender, receiver)
    # send('has entered the room.', room=roomId)
    send({'type': 'chat_messages', 'data': chat_history}, room=roomId)


@ socketio.on('leave')
def on_leave(data):
    sender = int(data['sender'])
    receiver = int(data['receiver'])
    roomId = get_chat_room_id(sender, receiver)
    leave_room(roomId)
    # send(username + ' has left the room.', room=room)


@ socketio.on('send')
def send_message(data):
    sender = int(data['sender'])
    receiver = int(data['receiver'])
    content = (data['content'])
    create_chat_message(sender, receiver, content)
    # // refresh
    roomId = get_chat_room_id(sender, receiver)
    chat_history = get_chat_history(sender, receiver)
    send({'type': 'chat_messages', 'data': chat_history}, room=roomId)
