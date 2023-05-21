from flask import Flask, jsonify, request, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists, and_
from setup import app, db, User
import json


@app.route("/api/user/login", methods=["POST"])
def user_login():
    body = json.loads(request.data)
    is_exist = db.session.query(exists().where(
        User.email == body["email"])).scalar()
    if is_exist == False:
        return jsonify({"success": False, "data": {}, "message": "Invalid email or password"})
    match_user = (
        db.session.query(User)
        .where(and_(User.email == body["email"], User.password == body["password"]))
        .all()
    )
    if len(match_user) == 0:
        return jsonify({"success": False, "data": {}, "message": "Invalid email or password"})
    resp = make_response(
        jsonify(
            {
                "success": True,
                "data": match_user[0].serialize,
                "message": "success",
            }
        )
    )
    session["userId"] = match_user[0].id
    return resp


@app.route("/api/user/register", methods=["POST"])
def user_register():
    body = json.loads(request.data)

    is_exist = db.session.query(exists().where(
        User.email == body["email"])).scalar()
    if is_exist == True:
        return jsonify({"success": False, "data": {}, "message": "User email already exists"})

    newUser = User(
        name=body.get("name"),
        email=body.get("email"),
        mobileNumber=body.get("mobileNumber"),
        password=body.get("password"),
    )
    db.session.add(newUser)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": newUser.serialize,
            "message": "sucess",
        }
    )


@app.route("/api/user/info", methods=["GET"])
def user_info():
    sessionID = session.get("userId")
    if sessionID:
        match_user = db.session.query(User).where(
            and_(User.id == sessionID)).all()
        if len(match_user) > 0:
            return jsonify(
                {
                    "success": True,
                    "data": match_user[0].serialize_private,
                    "message": "sucess",
                }
            )
    response = jsonify({"success": False, 'message': 'Unauthorized'})
    return response, 401


@app.route('/api/users/chat', methods=["GET"])
def chat_users():
    sessionID = session.get("userId")
    users = db.session.query(User).all()
    users_s = [i.serialize_private for i in users]
    filter_users = list(filter(lambda n: n['id'] != sessionID, users_s))
    return jsonify(
        {
            "success": True,
            "data": filter_users,
            "message": "sucess",
        }
    )


@app.route('/api/user/logout', methods=["POST"])
def user_logout():
    if session.get('userId'):
        session.pop('userId')
    return jsonify(
        {
            "success": True,
            "data": {},
            "message": "sucess",
        }
    )
