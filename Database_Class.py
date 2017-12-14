import psycopg2
import sys
import psycopg2.extras
from psycopg2 import sql
from config_example import *
from Classes_for_Data import *

class Database(object):
    
    def __init__(self):
        self.db_connection, self.db_cursor = self.get_connection_and_cursor()

    def get_connection_and_cursor(self):
        try:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        except:
            print("Unable to connect to the database. Check server and credentials.")
            sys.exit(1) # Stop running program if there's no db connection.
        db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return db_connection, db_cursor

    def setup_db(self):
        
        self.db_cursor.execute("DROP SCHEMA public CASCADE")
        self.db_cursor.execute("CREATE SCHEMA public")

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS SCHOOLS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(100) UNIQUE,
            CITY VARCHAR(50),
            STATE VARCHAR(50)
            )""")

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS RESTAURANTS (
            ID SERIAL PRIMARY KEY,
            YELP_ID VARCHAR(100) UNIQUE,
            NAME VARCHAR(100),
            SCHOOL_ID INTEGER REFERENCES SCHOOLS(ID),
            RATING REAL,
            DISTANCE REAL,
            PRICE VARCHAR(10)
            )
            """)

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            ID SERIAL PRIMARY KEY,
            RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID),
            TRANSACTION VARCHAR(50)
            )""")

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS CATEGORIES (
            ID SERIAL PRIMARY KEY,
            RESTAURANT_ID INTEGER REFERENCES RESTAURANTS(ID),
            CATEGORY VARCHAR(100)
            )""")

        self.db_connection.commit()
        print("*******Setup Success********** ")

    def insert(self, table, data_dict, no_return=False):  # data_dict = retaurant.get_dict()
        """Accepts connection and cursor, table name, dictionary that represents one row, and inserts data into table. (Not the only way to do this!)"""
        column_names = data_dict.keys()
        #print(column_names, "column_names") # for debug
        if not no_return:
            query = sql.SQL('INSERT INTO {0}({1}) VALUES({2}) ON CONFLICT DO NOTHING RETURNING id').format(
                sql.SQL(table),
                sql.SQL(', ').join(map(sql.Identifier, column_names)),
                sql.SQL(', ').join(map(sql.Placeholder, column_names))
            )
        else:
            query = sql.SQL('INSERT INTO {0}({1}) VALUES({2}) ON CONFLICT DO NOTHING').format(
                sql.SQL(table),
                sql.SQL(', ').join(map(sql.Identifier, column_names)),
                sql.SQL(', ').join(map(sql.Placeholder, column_names))
            )
        query_string = query.as_string(self.db_connection) # thanks to sql module
        self.db_cursor.execute(query_string, data_dict) # will mean that id is in cursor, because insert statement returns id in this function
        if not no_return:
            return self.db_cursor.fetchone()['id']

    def insert_Catego(self, data_dict, restaur_id): # data_dict is from restaurant.get_Transc_dict()
        catego_ls = data_dict['categories']
        for catego in catego_ls:
            cur_dict = {'restaurant_id': restaur_id, 'category': catego['title']}
            self.insert('categories', cur_dict)

    def insert_Transc(self, data_dict, restaur_id):
        transc_ls = data_dict['transactions']
        for transc in transc_ls:
            cur_dict = {'restaurant_id': restaur_id, 'transaction': transc}
            self.insert('transactions', cur_dict)

    def insert_One_Request(self, dict_ls, school_name): # dict_ls is the dict_ls returned by API
        school_dict = dict_ls[1]
        cur_school = School(school_name, school_dict)
        school_id = self.insert('schools', cur_school.get_School_dict())
        for one_restaur in dict_ls:
            cur_restaur = Restaurant(one_restaur, school_id, school_name)
            restaur_id = self.insert('restaurants', cur_restaur.get_Restaur_dict())
            self.insert_Catego(cur_restaur.get_Catego_dict(), restaur_id)
            self.insert_Transc(cur_restaur.get_Transc_dict(), restaur_id)
        self.db_connection.commit()
        print("*****Successfully Insert One Request to DB*******")

    def get_school_ls(self):
        self.db_cursor.execute("SELECT DISTINCT NAME FROM SCHOOLS ")
        school_ls = self.db_cursor.fetchall() # [{'name': 'columbia university'}, {'name': 'mit'}, {'name': 'umich'}, {'name': 'ucla'}, {'name': 'UT Austin'}]
        return school_ls

    def get_pop_num(self):
        self.db_cursor.execute("""SELECT COUNT(*) FROM RESTAURANTS WHERE RATING >= 4""")
        pop_num = self.db_cursor.fetchone()['count']
        return pop_num

    def avg_Rating(self):
        # print(type(self.db_cursor.fetchall()))
        school_ls = self.get_school_ls()
        # print(type(school_ls[0]['name']))
        avg_Rating_ls = []
        corresp_school_ls = []
        for school in school_ls:
            self.db_cursor.execute("""SELECT AVG(RATING) FROM RESTAURANTS INNER JOIN SCHOOLS 
                ON (RESTAURANTS.SCHOOL_ID = SCHOOLS.ID) WHERE SCHOOLS.NAME = '{}' """.format(school['name']))
            corresp_school_ls.append(school['name'])
            avg_Rating_ls.append(self.db_cursor.fetchone()['avg'])
        # print(avg_Rating_ls)
        return corresp_school_ls, avg_Rating_ls

    def percent_above_4(self):
        school_ls = self.get_school_ls()
        percent_4_ls = []
        corresp_school_ls = []
        for school in school_ls:
            self.db_cursor.execute("""SELECT COUNT(*) FROM RESTAURANTS INNER JOIN SCHOOLS 
                ON (RESTAURANTS.SCHOOL_ID = SCHOOLS.ID) WHERE RATING >= 4 AND SCHOOLS.NAME = '{}' """.format(school['name']))
            corresp_school_ls.append(school['name'])
            percent_4_ls.append(self.db_cursor.fetchone()['count'] / 50)
        # print(percent_4_ls)
        return corresp_school_ls, percent_4_ls
    
    def popular_category(self):
        pop_num = self.get_pop_num()

        self.db_cursor.execute("""SELECT CATEGORY, COUNT(*) FROM CATEGORIES INNER JOIN RESTAURANTS 
            ON (CATEGORIES.RESTAURANT_ID = RESTAURANTS.ID) WHERE RATING >= 4
            GROUP BY CATEGORY HAVING COUNT(*) > 20 ORDER BY COUNT(*) DESC""")
        pop_categ_ls = self.db_cursor.fetchall()
        
        pop_categ_name_ls = []
        pop_categ_ratio_ls = []
        remain_num = pop_num
        for category in pop_categ_ls:
            categ_name = category['category']
            count = category['count']
            remain_num -= count
            pop_categ_name_ls.append(categ_name)
            pop_categ_ratio_ls.append(count / pop_num)
        pop_categ_name_ls.append('Others')
        pop_categ_ratio_ls.append(remain_num / pop_num)
        return pop_categ_name_ls, pop_categ_ratio_ls

    def transc_service(self):
        pop_num = self.get_pop_num()
        self.db_cursor.execute("""SELECT COUNT(DISTINCT RESTAURANTS.ID) FROM RESTAURANTS INNER JOIN TRANSACTIONS
            ON (RESTAURANTS.ID = TRANSACTIONS.RESTAURANT_ID) WHERE RATING >= 4""")
        res_num = self.db_cursor.fetchone()['count']
        res = res_num / pop_num
        return ['w/ Service', 'w/o Service'], [res, 1 - res]

    def price_level(self):
        price_ls = ['$', '$$', '$$$', '$$$$']
        percent_ls = []
        for price in price_ls:
            self.db_cursor.execute("""SELECT COUNT(*) FROM RESTAURANTS WHERE PRICE = '{}'""".format(price))
            percent_ls.append(self.db_cursor.fetchone()['count'] / 250)
        # print(percent_ls)
        return price_ls, percent_ls

    def close_connection(self):
        self.db_connection.close()
