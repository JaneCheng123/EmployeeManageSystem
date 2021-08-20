import time
import pymysql
import threading
from DBUtils.PooledDB import PooledDB, SharedDBConnection

# connection pool with MySQL
POOL = PooledDB(
    creator=pymysql, 
    maxconnections=5, 
    mincached=2,
    maxshared=100,
    maxcached=100, 
    blocking=True, 
    maxusage=None, 
    setsession=[], 
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='xxyxxy',
    database='djangomysql',
    charset='utf8',
    autocommit=True,
)


def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor

 

def close_conn(conn,cursor):
    cursor.close()
    conn.close()
    

def insert(sql,args):
    conn,cursor = create_conn()
    res = cursor.execute(sql,args)
    conn.commit()
    close_conn(conn,cursor)
    return res

def delete(sql,args):
    conn,cursor = create_conn()
    res = cursor.execute(sql,args)
    conn.commit()
    close_conn(conn,cursor)
    return res

def update(sql,args):
    conn,cursor = create_conn()
    res = cursor.execute(sql,args)
    print("before commit")
    conn.commit()
    print("after commit")
    close_conn(conn,cursor)
    return res


def fetch_one(sql,args):
    conn,cursor = create_conn()
    cursor.execute(sql,args)
    res = cursor.fetchone()
    close_conn(conn,cursor)
    return res



def fetch_all(sql,args):
    conn,cursor = create_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res

def fetch_all(sql,args):
    conn,cursor = create_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res


# sql = "INSERT into salaries_salary (employeeid,name,age,department,hiredate,salary,level,subsidy,total) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# res = insert(sql,("100001","Chris","21","Testing","2020-01-01","5000","3","500","5500"))
