
from flask_restful import Api, Resource, reqparse
from flask import request, abort, jsonify, send_file
import db
import util
import json
import os
from datetime import datetime
from util import generateUUID, hashMD5
import app
from flask_cors import CORS

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


#for leasing
leasing_args_post = reqparse.RequestParser()
leasing_addargs_post= reqparse.RequestParser()
#
# leasing_addargs_post.add_argument('security_deposit', type=str, help='Missing Lessor ID', required=True)
# leasing_addargs_post.add_argument('improvements', type=str, help='Missing Lessee ID', required=True)
# leasing_addargs_post.add_argument('erect_signage', type=str, help='Missing Lessee ID', required=True)

# leasing_args_post.add_argument('lessorID', type=str, help='Missing Lessor ID', required=True)
# leasing_args_post.add_argument('lesseeID', type=str, help='Missing Lessee ID', required=True)
# leasing_args_post.add_argument('propertyID', type=str, help='Missing Property ID', required=True)

leasing_args_post.add_argument('leasing_status', type=str, help='Missing Leasing Status', required=True)
leasing_args_post.add_argument('leasing_start', type=str, help='Missing Leasing Start', required=True)
leasing_args_post.add_argument('leasing_end', type=str, help='Missing Leasing End', required=True)
leasing_args_post.add_argument('leasing_payment_frequency', type=str, help='Missing Payment Frequency', required=True)
leasing_args_post.add_argument('leasing_total_fee', type=str, help='Missing Total Fee', required=True)

# leasing_args_post.add_argument('leasing_remarks', type=str, help='Missing Leasing Remarks', required=False)
leasing_docs = reqparse.RequestParser()
leasing_docs.add_argument('leasingID', type=str, help='Missing Leasing ID', required=True)

#for messages
message_post = reqparse.RequestParser()
message_post.add_argument('msg_senderID', type=str, help='Missing Sender ID', required=True)
message_post.add_argument('msg_receiverID', type=str, help='Missing Receiver ID', required=True)
message_post.add_argument('msg_content', type=str, help='Missing Message Content', required=False)
message_post.add_argument('sent_at', type=str, help='Missing Time of Sending',required=True)

#for message images

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
        

class Leasing(Resource):
    def get(self):
        #get specific data
        userID = request.args.get('userID')
        #as a lessee
        leasingInfo = db.join_tables(userID)
        if leasingInfo is not None:
            leasing_encoded = json.dumps(leasingInfo,default=str)
            return leasing_encoded, 200
        else:
            return abort(400,'No conversations found')

    # def get(self):
    #     #get specific data
    #     leasingID = request.args.get('leasingID')
    #     leasingInfo = db.get_data('leasing', 'leasingID', leasingID)
    #     if leasingInfo is not None:
    #         leasing_encoded = json.dumps(leasingInfo,default=str)
    #         print(leasing_encoded)
    #         return leasing_encoded, 200
    #     else:
    #         return abort(400,'User not found')

    def post(self):
        leasingInfo = leasing_args_post.parse_args()
        #leasingInfo = request.get_json(force=True)
        
        param = str(leasingInfo['leasing_status']+leasingInfo['leasing_start']+leasingInfo['leasing_end']+leasingInfo['leasing_payment_frequency']+leasingInfo['leasing_total_fee'])
        leasingID = util.generateUUID(param)
        
        fields = ['leasingID','lessorID','lesseeID','propertyID']
        data = [leasingID,'1232','1231','1234']  

        for k,v in leasingInfo.items():
            fields.append(k)
            data.append(v)

        check_existing = db.check_existing_data('leasing', 'leasingID', fields[0])
        if check_existing:
            return {'message':f'User with userID: {leasingID} already exist'},409
        
        else:
            insert_data_bool = db.insert_data('leasing',fields,data)
            
            if insert_data_bool:

                #after inserting important leasing data, render the pdf(contract) and 
                # save the contract details to leasing_documents

                leasing_docID = util.createPDF(leasingID)
                leasing_doc_name = str(leasing_docID + "_contract.pdf") 
                insert_docs = db.insert_data('leasing_documents',['leasing_docID','leasingID','leasing_doc_name'],[leasing_docID,leasingID,leasing_doc_name])
                
                if insert_docs:
                    return {'message':'Successfully requested to lease'}, 201

            else:
                return {'message':'Unable to lease request'},400
            
        
    def delete(self):
        leasingID = request.args.get('leasingID')

        check_existing = db.check_existing_data('leasing', 'leasingID', leasingID)
        if check_existing:
            delete_user = db.delete_data('leasing', 'leasingID', leasingID)
            if delete_user:
                return {
                    'message': f'Leasing ID:{leasingID} is deleted'
                }, 200
            else:
                return{
                    'message':f'Error deleting lease contract:{leasingID}'
                }, 400
        else:
            return abort(400,'Cannot delete. Contract not found')
        
    
class Leasing_Documents(Resource):
    def get(self):
        #leasingID = request.args.get('leasingID')
        leasingID= '30de93a0c7013ed3bc403092b8d709bf'
        leasingDocs = db.get_data('leasing_documents', 'leasingID', leasingID)
        
        if leasingDocs is not None:
            file_path = f"static\{leasingID}\{leasingDocs['leasing_doc_name']}"
            return send_file(file_path, attachment_filename=os.path.basename(file_path), as_attachment=False)
        else:
            return abort(400,'Contract not found')
    
    def delete(self):
        return None
    
class Message(Resource):
    def get(self):
        leasingID = 'fasdfsdfdsfds'
        messages = db.get_items('message','leasingID', leasingID)
        if messages is not None:
            messages_encoded = json.dumps(messages,default=str)
            return messages_encoded, 200
        else:
            return abort(400,'No conversations found')
        


    def post(self):
        messageInfo = message_post.parse_args()
        
        fields = ['msgID','leasingID','msg_senderID','msg_receiverID','msg_content','sent_at']
        msgID = util.generateUUID(json.dumps(messageInfo))

        #values = [msgID, ]

        message = db.insert_data('messages',[''])
        app.socketio.emit('new-message', message.content, broadcast=True)
        return jsonify({'success': True})
    

class Message_Images(Resource):
    def get(self):
        return None
    def post(self):
        return None
#=======================================================================================


        
        
    
