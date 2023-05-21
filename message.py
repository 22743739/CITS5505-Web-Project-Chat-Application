from flask import Flask, jsonify, request, session
from sqlalchemy.sql import and_, or_
from sqlalchemy.orm import aliased

from setup import app, db, User, Message


@app.route("/api/search", methods=["GET"])
def search_message():
    keyword = request.args.get('keyword')
    userId = session.get("userId")
    receiverUser = aliased(User)
    senderUser = aliased(User)

    if userId:
        all = (
            db.session.query(Message)
            .join(receiverUser, (Message.receiver == receiverUser.id), isouter=True)
            .add_columns(receiverUser)
            .join(senderUser, (Message.sender == senderUser.id), isouter=True)
            .add_columns(senderUser)
            .order_by(Message.createAt.asc())
            .filter(and_(Message.content.like('%' + keyword + '%'),
                         or_(Message.sender == userId, Message.receiver == userId)))
            .order_by(Message.createAt.asc())
            .all()
        )
        list = []
        for i in all:
            item = {}
            item.update(i[0].serialize)
            item.update(
                {'receiverInfo': i[1].serialize_private if i[1] else {}})
            item.update({'senderInfo': i[2].serialize_private if i[2] else {}})
            list.append(item)
        return jsonify(
            {
                "success": True,
                "data": list,
                "message": "sucess",
            }
        )
    response = jsonify({"success": False, 'message': 'Unauthorized'})
    return response, 401
