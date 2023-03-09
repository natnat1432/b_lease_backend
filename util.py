import uuid
import hashlib
import datetime
import json
import decimal
import random


def generateUUID(input:str)->str:
    final_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, input)).replace("-", "")
    return final_id


def hashMD5(input:str):
    hashed =  hashlib.md5(input.encode())

    return str(hashed.hexdigest())


def generate_otp():
    otp = ""
    for i in range(6):
        otp+=str(random.randint(1,9))
    
    return otp

class JSONEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        elif isinstance(z, datetime.date):
            return (str(z))
        elif isinstance(z, decimal.Decimal):
            return str(z)
        else:
            return super().default(z)
        
