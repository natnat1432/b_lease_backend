
from http.client import HTTPResponse
from flask_restful import Api, Resource, reqparse
from flask import request, abort, jsonify
import db
import json
from datetime import datetime, timedelta
from util import generateUUID, hashMD5, JSONEncoder, generate_otp
from emailverification import email_verification
from apscheduler.schedulers.background import BlockingScheduler
from flask_cors import CORS

\
# signup_put_args = reqparse.RequestParser()
# signup_put_args.add_argument("contact_number", type=str, help="Phone number of the user")


# class signup(Resource):
#     def get(self):
#         return {'data':'hello'}
#     def put(self,id):
#         args = signup_put_args.parse_args()
#         return { id:args}



#REGISTER API CLASS
#=======================================================================================
register_args = reqparse.RequestParser()
register_args.add_argument('email', type=str, help='Missing Email', required=True)
otp_dict = {}



class register(Resource):
    def get(self):
        email = str(request.args.get('email'))
        otp = str(request.args.get('otp'))
        isFound = False

        print(otp_dict)
        for k,v in otp_dict.items():
            if k == email and v == otp:
                isFound=True
        
        if isFound:
            del otp_dict[email]
            print(otp_dict)
            return {'message':'OTP found'},200
        else:   
            return {'message':'OTP not found'},200
    def post(self):
        registerInfo = register_args.parse_args()

        email = request.json
        otp = generate_otp()

        send_email = email_verification(email['email'], otp)
       
        if send_email == True:
            otp_dict[email['email']] = otp
            print(otp_dict)
            return {'message':'success'},200
        else:
            return {'message':'error'},200
        
        
    def put(self):
        pass
    def delete(self):
        email = request.args.get('email')

        if email:
            if email in otp_dict:
                otp = otp_dict[email]
                otp_dict.pop(email,None)
                print(otp_dict)

                return {'message':f'OTP {otp} has expired '},200
            else:
              return abort(404,"OTP not found")  
        else:
            return abort(404,"OTP not found")
#=======================================================================================

#USER API CLASS
#=======================================================================================
user_args = reqparse.RequestParser()
user_args.add_argument('phone_number', type=str,help='Missing Phone number', required=True)
user_args.add_argument('user_password', type=str,help='Missing User password', required=True)
user_args.add_argument('user_fname', type=str,help='Missing User firstname', required=True)
user_args.add_argument('user_mname', type=str,help='Missing User middlename')
user_args.add_argument('user_lname', type=str,help='Missing User lastname', required=True)
user_args.add_argument('user_birthdate', type=str,help='Missing User birthdate', required=True)
user_args.add_argument('user_email', type=str,help='Missing User email',required=True)
user_args.add_argument('address', type=str,help='Missing User address', required=True)
user_args.add_argument('latitude', type=str,help='Missing Google maps latitude coordinate', required=True)
user_args.add_argument('longitude', type=str,help='Missing Google maps longitutde coordinate', required=True)

user_args_put = reqparse.RequestParser()
user_args_put.add_argument('userID', type=str, help='Missing User ID', required=True)

class user(Resource):
    def get(self):
        userID = request.args.get('userID')
        if userID is None:
            userInfo = db.get_all_data('user')
            userJson = json.dumps(userInfo, indent=2, cls=JSONEncoder)
            return userJson, 200
        else:
            if userID is not None:
                userInfo = db.get_data('user','userID',userID)
                userJson = json.dumps(userInfo,default=str)
          
                return jsonify(userJson)
               
            else:
                return abort(400,'User not found')
    
    def post(self):
        userInfo = user_args.parse_args()

        userJson = request.json
        userID = None
        fields = []
        data = []        
        for k,v in userJson.items():
            if v is not None:
                if k == 'phone_number':
                    fields.append('userID')
                    userID = generateUUID(json.dumps(userJson))
                    data.append(userID)
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
        print(fields)
        print(data)
        check_existing = db.check_existing_data('user', 'userID', userID)
        if check_existing:
            return {'message':f'User with userID: {userID} already exist'},409
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
#  LOGIN API CLASS | C 
login_args = reqparse.RequestParser()
login_args.add_argument('user_email', type=str, help='Missing Email', required=True)
login_args.add_argument('user_password', type=str, help='Missing Password', required=True)
login_args.add_argument('user_ip', type=str, help='Missing IP Address', required=True)

class login(Resource):
 def post(self):
        loginInfo = login_args.parse_args()

        loginJson = request.json
        sessionID = generateUUID(json.dumps(loginJson)+str(datetime.now()))
        userIP = None
        fields = []
        data = []     

        for k,v in loginJson.items():
                if k == 'user_password':
                    fields.append('user_password_hashed')
                    data.append(hashMD5(v))
                if k != 'user_ip':
                    fields.append(k)
                    data.append(v)

                if k == 'user_ip':
                    userIP = v

        print(fields)
        print(data)

        check_credential = db.get_specific_data('user', fields, data )

        if check_credential:
            session_fields = []
            session_data = []

            session_fields.append('sessionID')
            session_fields.append('userID')
            session_fields.append('loginTime')
            session_fields.append('ipAddress')
            session_fields.append('status')
    
            session_data.append(sessionID)
            session_data.append(check_credential['userID'])
            session_data.append(str(datetime.now()))
            session_data.append(userIP)
            session_data.append('valid')

            create_session = db.insert_data('session',session_fields, session_data)

            if create_session:

                return {'message':'Login',
                        'sessionID':sessionID,
                        'userID':check_credential['userID']
                        },200
            else:
                return abort(404, 'Error creating session')
        else:
            return {'message':'Invalid Credentials'},404
        # if check_existing:
        #     return {'message':f'User with userID: {userID} already exist'},409
        # else:
        #     insert_data_bool = db.insert_data('user',fields,data)
        #     if insert_data_bool:
        #         return {'message':'Success user creation'},201
        #     else:
        #         return {'message':'Error user creation'},400
#=======================================================================================

# SESSION API CLASS | CRU
session_args = reqparse.RequestParser()
session_args.add_argument('sessionID', type=str, help='Missing Session ID', required=True)
session_args.add_argument('userID', type=str, help='Missing User ID', required=True)
session_args.add_argument('ipAddress', type=str, help='Missing device IP Address', required=True)

class session(Resource):
    def get(self):
        sessionID = request.args.get('sessionID')
        sessionInfo = db.get_data('session', 'sessionID', sessionID)
        if sessionInfo is not None:
            userJson = json.dumps(sessionInfo,default=str)
            print(userJson)
            return userJson, 200
        else:
            return abort(400,'Session not found')
    def post(self):
        sessionInfo = session_args.parse_args()

        sessionJson = request.json
        fields = []
        data = []        
        for k,v in sessionJson.items():
            if v is not None:
                if k == 'userID':
                    fields.append('loginTime')
                    data.append(str(datetime.now()))
                fields.append(k)
                data.append(v)
        fields.append('status')
        data.append('open')

        check_existing= db.check_existing_data('session', 'sessionID', sessionJson['sessionID'])
        if check_existing:
            return {'message':f'Session with sessionID: {sessionJson["sessionID"]} already exist'},409
        else:

            check_existing_user = db.check_existing_data('user', 'userID', sessionJson['userID'])
            if check_existing_user:
                insert_data_bool = db.insert_data('session',fields,data)
                if insert_data_bool:
                    return {'message':'Success session creation'},201
                else:
                    return {'message':'Error session creation'},400
            else:
                return abort(400,'User does not exist')
    def put(self):
        sessionInfo = session_args.parse_args()

        sessionJson = request.json
        fields = []
        data = []        
        for k,v in sessionJson.items():
            if v is not None:
                fields.append(k)
                data.append(v)

        for i in range(len(data)):
            if data[i] == 'open':
                data[i] = 'closed'
        

        check_existing= db.check_existing_data('session', 'sessionID', sessionJson['sessionID'])
        if check_existing:
            check_existing_user = db.check_existing_data('user', 'userID', sessionJson['userID'])
            if check_existing_user:
                update_data_bool = db.update_data('session',fields,data)
                if update_data_bool:
                    return {'message':'Success session update'},201
                else:
                    return {'message':'Error session update'},400
            else:
                return abort(400,'User does not exist') 
        else:
            return {'message':f'Session with sessionID: {sessionJson["sessionID"]} does not exist'},409
           
    
#=======================================================================================
# NOTIFICATION API CLASS | CRU
    
#=======================================================================================
# PAYMENT API CLASS | CRU

#=======================================================================================
# USER PAYMENT METHOD API CLASS | CRUD

upm_args = reqparse.RequestParser()
upm_args.add_argument('userID', type=str, help='Missing UserID', required=True)
upm_args.add_argument('userPay_accName', type=str, help='Missing Account Name', required=True)
upm_args.add_argument('userPay_accNum', type=str, help='Missing Account Number', required=True)
class user_payment_method(Resource):

    def get(self):
        pass
    def post(self):
        upmInfo = upm_args.parse_args()
        upmJson = request.json

        fields = []
        data = []
        paymethodID = json.dumps(upmJson)
        paymethodID = generateUUID(paymethodID)

        fields.append('paymethodID')
        data.append(paymethodID)
        for k,v in upmJson.items():
            if v is not None:
                fields.append(k)
                data.append(v)
                if k == 'userPay_accName':
                    fields.append('userPay_dateAdded')
                    data.append(str(datetime.now()))
        print(fields)
        print(data)
    def put(self):
        pass
    def delete(self):
        pass
#=======================================================================================
# COMPLAINT API CLASS | CR
complaint_args = reqparse.RequestParser()
complaint_args.add_argument('complaint_categ', type=str, help='Missing Complaint Category', required=True)
complaint_args.add_argument('complaint_desc', type=str, help='Missing Complaint Description', required=True)
complaint_args.add_argument('complainerID', type=str, help='Missing ComplainerID', required=True)
complaint_args.add_argument('complaineeID', type=str, help='Missing ComplaineeID', required=True)


class complaint(Resource):
    def get(self):
        complainerID = request.args.get('complainerID')
        if complainerID is None:
            return abort(400, 'Missing complainer ID')
        else:
            complaints = db.get_data('complaint', 'complainerID', complainerID)
            if complaints:
                userJson = json.dumps(complaints, indent=2, cls=JSONEncoder)
                return userJson, 200
            else:
                return {'message':'No complaints found'}
    def post(self):
        complaintInfo = complaint_args.parse_args()
        complaintJson = request.json

        complaintID = json.dumps(complaintJson)
        complaintID = generateUUID(complaintID+str(datetime.now()))

        fields = []
        data = []        
        complainerID = ""
        complaineeID = ""
        for k,v in complaintJson.items():
            if v is not None:
                if k == 'complaint_categ':
                    fields.append('complaintID')
                    data.append(complaintID)
                fields.append(k)
                data.append(v)

                if k == 'complainerID':
                    complainerID = v
                if k == 'complaineeID':
                    complaineeID = v


        check_pending_complaint = db.get_specific_data('complaint',['complainerID','complaineeID','complaint_status'],[complainerID,complaineeID,'pending'])
        if check_pending_complaint:
            return abort(400,'There is still pending complaint. Wait for complaint to be resolved')
        else:
            fields.append('complaint_status')
            data.append('pending')

            
            fields.append('created_at')
            data.append(str(datetime.now()))
            
            check_existing= db.check_existing_data('complaint', 'complaintID', complaintID)
            if check_existing:
                return {'message':f'Complaint with complaintID: {complaintID} already exist'},409
            else:

                check_complainer = db.check_existing_data('user', 'userID', complainerID)
                check_complainee = db.check_existing_data('user', 'userID', complaineeID)
                if check_complainer and check_complainee:
                    insert_data_bool = db.insert_data('complaint',fields,data)
                    if insert_data_bool:
                        return {'message':'Success complaint creation'},201
                    else:
                        return {'message':'Error complaint creation'},400
                else:
                    warn = ""
                    complainer_msg = "Complainer does not exist."
                    complainee_msg = "Complainee does not exist."
                    if check_complainer:
                        warn = warn + complainer_msg
                    if check_complainee:
                        warn = warn + complainee_msg
                    return abort(400,warn)

#=======================================================================================
# ADMIN API CLASS | CRUD
    
#=======================================================================================