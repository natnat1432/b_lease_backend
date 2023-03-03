
from flask_restful import Api, Resource, reqparse
from flask import request, abort, jsonify
import db
import json
from datetime import datetime
from util import generateUUID, hashMD5




# signup_put_args = reqparse.RequestParser()
# signup_put_args.add_argument("contact_number", type=str, help="Phone number of the user")


# class signup(Resource):
#     def get(self):
#         return {'data':'hello'}
#     def put(self,id):
#         args = signup_put_args.parse_args()
#         return { id:args}

user_args = reqparse.RequestParser()
user_args.add_argument('userID', type=str,help='Missing User ID', required=True)
user_args.add_argument('phone_number', type=str,help='Missing Phone number', required=True)
user_args.add_argument('user_password', type=str,help='Missing User password', required=True)
user_args.add_argument('user_fname', type=str,help='Missing User firstname', required=True)
user_args.add_argument('user_mname', type=str,help='Missing User middlename')
user_args.add_argument('user_lname', type=str,help='Missing User lastname', required=True)
user_args.add_argument('user_birthdate', type=str,help='Missing User birthdate', required=True)
user_args.add_argument('user_email', type=str,help='Missing User email')
user_args.add_argument('address', type=str,help='Missing User address', required=True)
user_args.add_argument('latitude', type=str,help='Missing Google maps latitude coordinate', required=True)
user_args.add_argument('longitude', type=str,help='Missing Google maps longitutde coordinate', required=True)

user_args_put = reqparse.RequestParser()
user_args_put.add_argument('userID', type=str, help='Missing User ID', required=True)



#USER API CLASS
#=======================================================================================
class user(Resource):
    def get(self):
        userID = request.args.get('userID')
        userInfo = db.get_data('user', 'userID', userID)
        if userInfo is not None:
            userJson = json.dumps(userInfo,default=str)
            print(userJson)
            return userJson, 200
        else:
            return abort(400,'User not found')
    
    def post(self):
        userInfo = user_args.parse_args()

        userJson = request.json
        
        fields = []
        data = []        
        for k,v in userJson.items():
            if v is not None:
                if k == 'user_password':
                    fields.append('user_password_hashed')
                    data.append(hashMD5(v))
                fields.append(k)
                data.append(v)

                if k == 'user_password':
                    fields.append('user_status')
                    data.append('active')
        fields.append('created_at')
        data.append(str(datetime.now()))

        check_existing = db.check_existing_data('user', 'userID', userJson['userID'])
        if check_existing:
            return {'message':f'User with userID: {userJson["userID"]} already exist'},409
        else:
            insert_data_bool = db.insert_data('user',fields,data)
            if insert_data_bool:
                return {'message':'Success user creation'},201
            else:
                return {'message':'Error user creation'},400

    def delete(self):
        userID = request.args.get('userID')

        check_existing = db.check_existing_data('user', 'userID', userID)
        if check_existing:
            delete_user = db.delete_data('user', 'userID', userID)
            if delete_user:
                return {
                    'message': f'User with UserID:{userID} is deleted'
                }, 200
            else:
                return{
                    'message':f'Error deleting user with UserID:{userID}'
                }, 400
        else:
            return abort(400,'Cannot delete. User not found')
    
    def put(self):
        userInfo = user_args_put.parse_args()

        userJson = request.json
        
        fields = []
        data = []
        
        for k,v in userJson.items():
            if v is not None:
                fields.append(k)
                data.append(v)
        

        check_existing = db.check_existing_data('user', 'userID', userJson['userID'])

        if check_existing:
            update_user = db.update_data('user', fields, data)
            
            if update_user:
                return {
                    'message': f"User with userID:{userJson['userID']} updated successfully"
                }, 200
            else:
                return{
                    'message': f"Error updating user with userID:{userJson['userID']}"
                },400
        else:
            return {'message':f'User with userID: {userJson["userID"]} does not exist'},400
        

#=======================================================================================


        
        
    
