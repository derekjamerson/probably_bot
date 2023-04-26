from utilities import connect_to_db


def create_table():
    cursor = connect_to_db()
    table = """
        CREATE TABLE customs_tracker (
            ID INTEGER PRIMARY_KEY,
            Name VARCHAR(50) NOT NULL,
            Wins INT(10) NOT NULL DEFAULT 0,
            Games INT(10) NOT NULL DEFAULT 0
        );
    """
    cursor.execute(table)


if __name__ == '__main__':
    create_table()
