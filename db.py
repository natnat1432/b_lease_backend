from flask_mysqldb import MySQL
from app import mysql


def get_all_data(table:str)->dict:
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT * FROM {table}''')
    data:dict = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data

def get_data(table:str, field:str, value:str)->dict:
    cur = mysql.connection.cursor() 
    cur.execute(f'''SELECT * FROM {table} WHERE `{field}` = "{value}" ''')
    data:dict = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data

def get_items(table:str, field:str, value:str)->dict:
    cur = mysql.connection.cursor() 
    cur.execute(f'SELECT * FROM {table} WHERE `{field}` = "{value}" ')
    data:dict = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data

def get_items_in_order(table:str, field:str, value:str, order_field:str, order:str)->dict:
    cur = mysql.connection.cursor() 
    cur.execute(f'SELECT * FROM {table} WHERE `{field}` = "{value}" ORDER BY {order_field} {order}')
    data:dict = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data

def check_existing_data(table:str, field:str, value:str)->bool:
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT EXISTS(SELECT * FROM `{table}` WHERE `{field}` = "{value}") AS check_existing''')
    data:bool = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data['check_existing']


def count_data(table:str)->dict:
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT COUNT(*) AS total FROM `{table}`''')
    data:dict = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data


def insert_data(table:str, fields, value)->bool:
    cur = mysql.connection.cursor()

    flds = '`,`'.join(fields)
    dta = ""
    last_item = value[-1]
    for each in value:
        if each != last_item:
            if type(each) == str:
                dta = dta + f'''"{each}",'''
            else:
                dta = dta + f'''{each},'''
        else:
            if type(each) == str:
                dta = dta + f'''"{each}"'''
            else:
                dta = dta + f'''{each}'''
    cur.execute(f'''INSERT INTO `{table}`(`{flds}`) VALUES({dta})''')
    mysql.connection.commit()
    cur.close()
    return True

def delete_data(table:str, field, value)->bool:
    cur = mysql.connection.cursor()
    cur.execute(f'''DELETE FROM `{table}` WHERE `{field}` = "{value}" ''')
    mysql.connection.commit()
    cur.close()
    return True

def update_data(table:str, fields, values)->bool:
    cur = mysql.connection.cursor()
    flds = []
    if len(fields) == len(values):
        for i in range(len(fields)):
            if type(values[i]) == str:
                flds.append(f'''`{fields[i]}` = "{values[i]}"''')
            else:
                flds.append(f'''`{fields[i]}` = {values[i]}''')
        flds_final = ", ".join(flds)
        cur.execute(f'''UPDATE `{table}` SET {flds_final} WHERE `{fields[0]}` = "{values[0]}"''')
        mysql.connection.commit()
        cur.close()
        return True
    else:
        return False


def get_specific_data(table:str, fields, values):
    cur = mysql.connection.cursor()
    flds = []
    
    if len(fields) == len(values):
        for i in range(len(fields)):
            if type(values[i]) == str:
                flds.append(f'''`{fields[i]}` = "{values[i]}"''')
            else:
                flds.append(f'''`{fields[i]}` = {values[i]}''')
            
        flds_final = " AND ".join(flds)
        cur.execute(f'''SELECT * FROM {table} WHERE {flds_final}''')
        data:dict = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return data

#not a database abstraction
#only used temporarily for getting the conversations per inquired property
def join_tables(userID:str):
    cur = mysql.connection.cursor() 
    cur.execute(f'''

        SELECT L.LEASINGID, U.USERID, U.USER_FNAME, P.ADDRESS
        FROM USER U, PROPERTY P, LEASING L
        WHERE ((L.LESSORID = '{userID}' AND U.USERID = L.LESSEEID) || (L.LESSEEID = '{userID}' AND U.USERID = L.LESSORID))
        AND L.PROPERTYID = P.PROPERTYID

    ''')


    data:dict = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data

# ORIGINAL QUERY

#         SELECT L.LEASINGID, U.USERID, U.USER_FNAME, P.ADDRESS, M.MSG_CONTENT
#         FROM USER U, PROPERTY P, LEASING L, MESSAGE M
#         WHERE M.MSG_CONTENT = (
#             SELECT M2.MSG_CONTENT FROM
#             MESSAGE M2, LEASING L
#             WHERE M2.LEASINGID = L.LEASINGID
#             ORDER BY M2.SENT_AT DESC
#             LIMIT 1
#         )
#         AND ((L.LESSORID = '{userID}' AND U.USERID = L.LESSEEID) || (L.LESSEEID = '{userID}' AND U.USERID = L.LESSORID))
#         AND L.PROPERTYID = P.PROPERTYID

        
