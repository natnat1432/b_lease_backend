from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_mysqldb import MySQL
import db







app = Flask(__name__)
app.secret_key = "b-lease2022"

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


   



    
@app.route("/")
def index():
    fields = [
        'adminID',
        'admin_fname',
        'admin_mname',
        'admin_lname',
        'admin_username',
        'admin_password_hashed',
        'admin_password',
    ]

    data = [
        'asdasd',
        'nathaniel',
        'Cabual',
        'Tiempo',
        'sdasjhkhkda',
        '1234567890',
        '1234567890'

    ]

    insert = db.insert_data('admin', fields, data)
    if insert:
        return "Success"
    else:
        return "Fail"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
