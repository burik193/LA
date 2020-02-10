import sqlite3
global path


#Under construnction
#Database creator

class DB:
    attributes = ''
    len_list = 0
    def __init__(self):
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()
        self.string = False


    def check_table(self, table):
        self.catch = False
        create_table = '''CREATE Table {} (num integer PRIMARY KEY)'''.format(table)
        try:
            self.c.execute(create_table)
            self.conn.commit()
        except sqlite3.Error as error:
            self.catch = True
        if not self.catch:
            self.delete_table(table)
            print('>> Connection name {} is free.'.format(table))
        return self.catch


    def create_table(self, table, list_of_datatypes):
        # list_of_datatypes = ['int', 'str']
        i = 0
        self.len_list = len(list_of_datatypes)
        columns = ''
        for type in list_of_datatypes:
            i = i+1
            attr = 'attr{}'.format(i)
            if type == 'int':
                columns = columns + ', {} integer'.format(attr)
            elif type == 'str':
                self.string = True
                columns = columns + ', {} text'.format(attr)
            elif type == 'float':
                columns = columns + ', {} real'.format(attr)
            self.attributes = self.attributes + ', ' + attr
        create_table = '''CREATE TABLE IF NOT EXISTS {} (num integer primary key {})'''.format(table, columns)
        try:
            self.c.execute(create_table)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to create a new table", error)

#muss verarbeitet werden
    def insert_data(self, table, num, *attr):
        value_str = str(num) + ', '
        if self.string:
            for a in attr:
                value_str = value_str + "\'" + str(a) + "\'" + ', '
            value_str = value_str.strip(', ')
        else:
            for a in attr[0]:
                value_str = value_str + str(a) + ', '
            value_str = value_str.strip(', ')
        insert_table = '''INSERT INTO {}(num {}) VALUES({})'''.format(table, self.attributes, value_str)
        try:
            self.c.execute(insert_table)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert data", error)


    def rewrite_data(self, table, num, attr, value):
        rewrite = '''Update {} set {} = {} where num = {}'''.format(table, attr, value, num)
        try:
            self.c.execute(rewrite)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert data", error)


    def get_table_names(self):
        table_names=[]
        try:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = self.c.fetchall()
        except sqlite3.Error as error:
            print("Failed to get table names", error)
        finally:
            return table_names


    def delete_table(self, table):
        drop_table = '''DROP TABLE IF EXISTS {};'''.format(table)
        try:
            self.c.execute(drop_table)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to delete a table", error)


    def get_table_data(self, table):
        table_data = []
        get_data = '''SELECT * FROM {}'''.format(table)
        try:
            self.c.execute(get_data)
            table_data = self.c.fetchall()
        except sqlite3.Error as error:
            print("Failed to get table data", error)
        finally:
            return table_data


    def db_close(self):
        if self.conn:
            self.conn.close()