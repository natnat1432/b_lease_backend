import uuid
import hashlib


def generateUUID(input:str)->str:
    final_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, input)).replace("-", "")
    return final_id


def hashMD5(input:str):
    hashed =  hashlib.md5(input.encode())

    return str(hashed.hexdigest())