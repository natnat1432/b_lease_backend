# from gevent import monkey
# monkey.patch_all()

from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_mysqldb import MySQL
from flask_restful import Api,Resource
import db
import restapi
from flask_cors import CORS
import json
from flask_socketio import SocketIO, send, emit
import datetime
import flask

app = Flask(__name__)
app.secret_key = "b-lease2022"
#==================
api = Api(app)

CORS(app)

socketio = SocketIO(app, async_mode='gevent', engineio_logger=True, cors_allowed_origins='*')
#socketio = SocketIO(app, cors_allowed_origins='*')
#----------------------------------------------------

api.add_resource(restapi.user,"/user")
api.add_resource(restapi.session,"/session")
api.add_resource(restapi.complaint,"/complaint")
api.add_resource(restapi.user_payment_method,"/user_payment_method")
api.add_resource(restapi.register,"/register")
api.add_resource(restapi.login,"/login")


api.add_resource(restapi.Leasing,"/leasing")
api.add_resource(restapi.Leasing_Documents,"/leasingdocs")
api.add_resource(restapi.Message,"/messages")
#-----------------------------------------------------

#Database Connection Setup 
#-----------------------------------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'allain19851047!'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DB'] = 'b_lease'
mysql = MySQL(app)
#-----------------------------------------------------


# @socketio.on('connect')
# def handle_connect():
#     emit('message', {'text': 'Connected from Server'})

@socketio.on('disconnect')
def handle_disconnect():
    emit('users-changed', {'user': 'allain', 'event': 'left'})

@socketio.on('set-nickname')
def handle_set_nickname(data):
    nickname = 'allain'
    emit('users-changed', {'user': nickname, 'event': 'joined'}, broadcast=True)
    flask.session['nickname'] = nickname

@socketio.on('add-message')
def handle_add_message(data):
    emit('message', {'leasingID': data['leasingID'], 'msg_senderID': data['msg_senderID'],'msg_receiverID': data['msg_receiverID'], 'msg_content': data['msg_content'], 'sent_at': data['sent_at']}, broadcast=True)

#, 'from': data['nickname'], 'created': data['created']

if __name__ == "__main__":
    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
    from geventwebsocket.handler import WebSocketHandler
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(('0.0.0.0', 5000,), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    #app.run(debug=True, host="0.0.0.0", port=5000,)




