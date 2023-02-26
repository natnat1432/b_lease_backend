from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_mysqldb import MySQL
from flask_restful import Api,Resource
import db
import restapi







app = Flask(__name__)
app.secret_key = "b-lease2022"

#Api setup
#-----------------------------------------------------


api = Api(app)
api.add_resource(restapi.user,"/user")
# api.add_resource(restapi.signup,"/signup/<string:id>")


#-----------------------------------------------------

#Database Connection Setup 
#-----------------------------------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@farmleaseoperationsmanagement2022'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DB'] = 'b_lease'
mysql = MySQL(app)
#-----------------------------------------------------








    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
