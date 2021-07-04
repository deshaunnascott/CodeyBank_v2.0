# =============================================================================
# Created By  : ShaunCodes
# Created Date: September 4, 2020
# =============================================================================
"""
This file contains the code to create Database Objects
"""
# =============================================================================
# Imports
# =============================================================================
import sqlite3
import os

# =============================================================================
# Class Definitions for Database
# =============================================================================
class Database:
    # Create database folder if it doesn't exist
    if not os.path.exists('./Database'):
        os.makedirs('./Database')

    # database location
    DB_LOCATION = './Database/mem_db.sqlite'

    def __init__(self, table_name="Members"):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cur = self.connection.cursor()
        self.table = table_name
        self.create_table(self.table)

    def close(self):
        """Close database connection"""
        self.connection.close()

    # create account table
    def create_table(self, tablename):
        create_acct_table = """
        CREATE TABLE IF NOT EXISTS {name} (
          acctNum INTEGER  PRIMARY KEY,
          pin INTEGER,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          checking_balance FLOAT,
          savings_balance FLOAT
        );""".format(name=tablename)

        # execute query
        self.cur.execute(create_acct_table)
        # commit changes
        self.connection.commit()

    def add_new_acct(self, table_name, acctObj):
        insert_query = """
        INSERT INTO
          {name} (acctNum, pin, first_name, last_name, checking_balance,savings_balance)
        VALUES
          ({acctNum}, {pin}, '{firstName}', '{lastName}', {checking_balance}, {savings_balance});
        """.format(name=table_name, acctNum=acctObj.acct_num, pin=acctObj.mem_pin, firstName=acctObj.mem_first_name,
                   lastName=acctObj.mem_last_name, checking_balance=acctObj.mem_cbalance,
                   savings_balance=acctObj.mem_sbalance)

        # execute query
        self.cur.execute(insert_query)
        # commit changes
        self.connection.commit()

    def delete_acct(self, table_name, acctNum):
        delete_query = """
        DELETE FROM
          {name}
        WHERE
          acctNum = {acct_id};
          """.format(name=table_name, acct_id=acctNum)

        # execute query
        self.cur.execute(delete_query)
        # commit changes
        self.connection.commit()

    def update_balance(self, table_name, acctNum, mem_acctType, mem_balance):
        update_query = """
        UPDATE
          {name}
        SET
          {acctType} = {acct_balance}
        WHERE
          acctNum = {acct_id};
        """.format(name=table_name, acctType=mem_acctType, acct_balance=mem_balance, acct_id=acctNum)

        # execute query
        self.cur.execute(update_query)

        # commit changes
        self.connection.commit()

    def update_account(self, table_name, acctNum, column, new_info):
        update_query = """
        UPDATE
          {name}
        SET
          {column} = '{new_info}'
        WHERE
          acctNum = {acct_id};
        """.format(name=table_name, column=column, new_info=new_info, acct_id=acctNum)

        # execute query
        self.cur.execute(update_query)

        # commit changes
        self.connection.commit()

    # function to check for member with id and pin at login
    def member_exists(self, table_name, acctNum_info, pin_info):
        select_query = """SELECT * FROM {table} 
        WHERE acctNum = {acctNum}
        AND pin = {pin};""".format(table=table_name, acctNum=acctNum_info, pin=pin_info)

        # execute query
        self.cur.execute(select_query)

        # get data from database
        data = self.cur.fetchone()

        if not data:
            return False  # data for member not found
        else:
            return True  # data found

    # search function for one column at a time
    def in_database(self, table_name, table_column, get_info):
        data = self.get_acct_info(table_name, table_column, get_info)

        if not data:
            return False  # data for column not found
        else:
            return True  # data found

    # find account and return the information found
    def get_acct_info(self, table_name, table_column, get_info):
        select_query = """SELECT * FROM {table} WHERE {column} = {info};""".format(table=table_name,
                                                                                   column=table_column, info=get_info)
        # execute query
        self.cur.execute(select_query)

        # get data from database
        data = self.cur.fetchone()

        return data
