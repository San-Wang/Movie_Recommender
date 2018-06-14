import MySQLdb

def connection():
    conn = MySQLdb.connect(
        host='localhost', #127.0.0.1
        user='root',
        passwd='930423',
        db='movies'
    )

    return conn


