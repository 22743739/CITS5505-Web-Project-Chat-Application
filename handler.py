from setup import db, User, Message
from sqlalchemy.sql import and_, or_
from sqlalchemy.orm import aliased


def get_chat_room_id(sender, receiver):
    if receiver == 0:
        return 'public'
    if int(sender) < int(receiver):
        return str(sender) + str(receiver)
    return str(receiver) + str(sender)


def get_chat_history(sender, receiver):
    print(sender, receiver)
    receiverUser = aliased(User)
    senderUser = aliased(User)

    all = []
    # public room
    if receiver == 0:
        all = (
            db.session.query(Message)
            .where(Message.receiver == receiver)
            .join(receiverUser, (Message.receiver == receiverUser.id), isouter=True)
            .add_columns(receiverUser)
            .join(senderUser, (Message.sender == senderUser.id), isouter=True)
            .add_columns(senderUser)
            .order_by(Message.createAt.asc())
            .all()
        )
    else:
        all = (
            db.session.query(Message)
            .where(or_(and_(Message.sender == sender, Message.receiver == receiver),
                       and_(Message.sender == receiver,
                            Message.receiver == sender)
                       ))
            .join(receiverUser, (Message.receiver == receiverUser.id), isouter=True)
            .add_columns(receiverUser)
            .join(senderUser, (Message.sender == senderUser.id), isouter=True)
            .add_columns(senderUser)
            .order_by(Message.createAt.asc())
            .all()
        )
    list = []
    for i in all:
        item = {}
        item.update(i[0].serialize)
        item.update({'receiverInfo': i[1].serialize_private if i[1] else {}})
        item.update({'senderInfo': i[2].serialize_private if i[2] else {}})

        list.append(item)
    return list


def create_chat_message(sender, receiver, content):
    newMessage = Message(
        sender=sender,
        receiver=receiver,
        content=content
    )
    db.session.add(newMessage)
    db.session.commit()
