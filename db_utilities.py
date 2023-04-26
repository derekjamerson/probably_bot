import sqlite3


def connect_to_db():
    return sqlite3.connect('./sqlite.db')


def insert_test_data():
    sql = """
        INSERT INTO Magic_Internet_Points ('Name', 'Wins', 'Games')
        VALUES
            ('Probably Test', 1, 5),
            ('Callmetest', 7, 44),
            ('xTheTest', 69, 69);
    """

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    print('rowcount', cursor.rowcount)
    print(list(cursor.execute("""SELECT * FROM Magic_Internet_Points""")))
