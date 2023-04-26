from db_utilities import connect_to_db


def create_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    table_mip = """
        CREATE TABLE Magic_Internet_Points (
            Name VARCHAR(50) NOT NULL,
            Wins INT(10) NOT NULL DEFAULT 0,
            Games INT(10) NOT NULL DEFAULT 0
        );
    """
    cursor.execute(table_mip)

    table_current_game = """
        CREATE TABLE Current_Game (
            Blue VARCHAR(300) NOT NULL,
            Red VARCHAR(300) NOT NULL
        );
    """
    cursor.execute(table_current_game)

    conn.close()


if __name__ == '__main__':
    create_table()
