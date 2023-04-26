import sqlite3



def create_table():
    conn = sqlite3.connect('./sqlite.db')
    cursor = conn.cursor()
    table = """
        CREATE TABLE `customs_tracker` (
            `ID` INT(10) NOT NULL AUTO_INCREMENT,
            `Name` VARCHAR(50) NOT NULL,
            `Wins` INT(10) NOT NULL DEFAULT '0',
            `Games` INT(10) NOT NULL DEFAULT '0',
            PRIMARY KEY (`ID`)
        );
    """
    cursor.execute(table)

if __name__ == '__main__':
    create_table()