import mysql.connector

class db_setup:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.__mydb =  mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.__cursor = self.__mydb.cursor()

    def __initialize(self):
        print("Initializing tables")
        self.__cursor.execute("""CREATE TABLE customers (
                                customer_id INT UNSIGNED AUTO_INCREMENT,
                                name VARCHAR(255),
                                age SMALLINT UNSIGNED,
                                joined_date DATE,
                                PRIMARY KEY(customer_id)
                                )""")

        self.__cursor.execute("""CREATE TABLE games (
                                product_id INT UNSIGNED AUTO_INCREMENT, 
                                name VARCHAR(255), 
                                genre VARCHAR(255),
                                pegi_rating SMALLINT UNSIGNED,
                                stock INT UNSIGNED,
                                PRIMARY KEY(product_id)
                                )""")

        self.__cursor.execute("""CREATE TABLE rented_games (
                                rental_id INT UNSIGNED AUTO_INCREMENT, 
                                customer_id INT UNSIGNED, 
                                product_id INT UNSIGNED,
                                rental_date DATETIME,
                                return_date DATETIME,
                                overdue BOOL,
                                PRIMARY KEY(rental_id)
                                )""")
        self.__mydb.commit()
        self.__terminate()

    def check(self):
        #check if tables etc. already exists, if yes -> terminate; else -> initialize
        print("Initialization check initiated!")
        self.__cursor.execute("""SELECT COUNT(*)
                                FROM information_schema.tables 
                                WHERE table_schema = DATABASE()
                                AND table_name IN ('customers', 'games', 'rented_games')
                                """)
        check = self.__cursor.fetchone()

        #Check if tables exist, if so no initialization required.
        #If all tables doesn't exist, user will be prompted with the option to drop remaining tables & re-init.
        if check[0] == 3:
            print("Tables are already initialized!")
            self.__terminate()
        elif check[0] >= 1:
            print("Tables partially initialized - Two tables exist\n")
            user_input = input("Do you wish to drop existing tables & reinitialize Y/N: ")
            if user_input == "Y" or user_input == "y" or user_input == "yes":
                user_input = input("Are you certain Y/N: ")
                if user_input == "Y" or user_input == "y" or user_input == "yes":
                    print("Dropping remaining tables")
                    self.__cursor.execute("DROP TABLE IF EXISTS customers;")
                    self.__cursor.execute("DROP TABLE IF EXISTS games;")
                    self.__cursor.execute("DROP TABLE IF EXISTS rented_games;")
                    self.__initialize()
            else:
                self.__terminate()
        else: 
            self.__initialize()

    def __terminate(self):
        print("Terminating database connection")
        self.__mydb.close()



if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    host = os.getenv("host")
    user = os.getenv("user")
    password = os.getenv("password")
    database = os.getenv("database")

    setup = db_setup(host, user, password, database)
    setup.check()