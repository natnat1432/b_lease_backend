from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_mysqldb import MySQL
from flask_restful import Api,Resource
import db
import restapi
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import requests


app = Flask(__name__)


app.secret_key = "b-lease2022"
#Api setup
#-----------------------------------------------------

CORS(app)
api = Api(app)
#CORS(app, origins="http://localhost:8100")

#socketio = SocketIO(app, cors_allowed_origins="*")
#----------------------------------------------------

api.add_resource(restapi.user,"/user")
# api.add_resource(restapi.signup,"/signup/<string:id>")

api.add_resource(restapi.Leasing,"/leasing")
api.add_resource(restapi.Leasing_Documents,"/leasingdocs")

api.add_resource(restapi.Message,"/message")
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)







# if __name__ == '__main__':
#     db.create_all()
#     socketio.run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))
