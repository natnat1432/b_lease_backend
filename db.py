from flask_mysqldb import MySQL
from app import mysql


def get_data(table:str, field:str, value:str)->dict:
    cur = mysql.connection.cursor() 
    cur.execute(f"SELECT * FROM {table} WHERE `{field}` = '{value}' ")
    data:dict = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data

def get_all_data(table:str)->dict:
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data:dict = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data

def count_data(table:str)->dict:
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) AS total FROM `{table}`")
    data:dict = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data


def insert_data(table:str, fields, value)->bool:
    cur = mysql.connection.cursor()

    flds = '`,`'.join(fields)
    dta = "','".join(value)
    cur.execute(f"INSERT INTO `{table}`(`{flds}`) VALUES('{dta}')")
    mysql.connection.commit()
    cur.close()
    return True

def delete_data(table:str, field, value)->bool:
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM `{table}` WHERE `{field}` = '{value}' ")
    mysql.connection.commit()
    cur.close()
    return True

def update_data(table:str, fields, values)->bool:
    cur = mysql.connection.cursor()
    flds = []
    if len(fields) == len(values):
        for i in range(len(fields)):
            flds.append(f"`{fields[i]}` = '{values[i]}'")
        flds_final = ", ".join(flds)
        cur.execute(f"UPDATE `{table}` SET {flds_final} WHERE `{fields[0]}` = '{values[0]}'")
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
            flds.append(f"`{fields[i]}` = '{values[i]}'")
        flds_final = " AND ".join(flds)
        cur.execute(f"SELECT * FROM {table} WHERE {flds_final}")
        data:dict = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return data

