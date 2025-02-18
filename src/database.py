'''
Two functions to load data into an SQLite or a PostgreSQL database.
'''

import sqlite3
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text

def load_into_database(new_product_data, product_data,review_data,database_path):
    '''
    Load data into an sqlite database
    :param new_product_data: pandas DataFrame just as outputed by get_information
    :param product_data: product DataFram just as outputed by preprocess_products
    :param review_data: review DataFrame just as outputed by process_reviews
    :param database_path: path to sqlite database
    '''
    try:
        sqlite_connection = sqlite3.connect(database_path)
        cursor = sqlite_connection.cursor()
        # Creating new products table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_products
            (
                title TEXT PRIMARY KEY,
                description TEXT,
                category TEXT,
                positive_reviews INTEGER,
                neutral_reviews INTEGER,
                negative_reviews INTEGER,
                average_price FLOAT,
                average_rating FLOAT,
                average_review_rating FLOAT,
                amount_of_verified_purchases INTEGER,
                rating_number INTEGER,
                review_number INTEGER,
                parent_ids TEXT
            );
        ''')

        new_product_data.to_sql("new_products", sqlite_connection, if_exists="append", index = False)

        # Creating products table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS products
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        parent_id TEXT,
                        title TEXT,
                        descriptions TEXT,
                        main_category TEXT,
                        average_rating FLOAT,
                        rating_number INTEGER,
                        price_euros FLOAT,
                        similarity_scores FLOAT,
                        new_product_title TEXT
                    );
                ''')
        product_data["new_product_title"] = "".join(new_product_data["title"].tolist())
        product_data.to_sql("products", sqlite_connection, if_exists="append", index=False)

        # Creating review table
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS reviews
                            (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                parent_id TEXT,
                                emotion TEXT,
                                emotion_score FLOAT,
                                rating FLOAT,
                                text TEXT,
                                user_id TEXT,
                                verified_purchase INTEGER
                            );
                        ''')
        review_data.to_sql("reviews", sqlite_connection, if_exists="append", index=False)

    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('SQLite Connection closed')


def load_into_postgres(new_product_data, product_data, review_data, db_connection_string):
    '''
        Load data into an sqlite database
        :param new_product_data: pandas DataFrame just as outputed by get_information
        :param product_data: product DataFram just as outputed by preprocess_products
        :param review_data: review DataFrame just as outputed by process_reviews
        :param db_connection_string: conection url to PostgreSQL database
        '''
    try:
        # Create database engine
        engine = create_engine(db_connection_string)
        connection = engine.connect()

        # Creating new products table
        create_new_products_table = '''
        CREATE TABLE IF NOT EXISTS new_products (
            title TEXT PRIMARY KEY,
            description TEXT,
            category TEXT,
            positive_reviews INTEGER,
            neutral_reviews INTEGER,
            negative_reviews INTEGER,
            average_price FLOAT,
            average_rating FLOAT,
            average_review_rating FLOAT,
            amount_of_verified_purchases INTEGER,
            rating_number INTEGER,
            review_number INTEGER,
            parent_ids TEXT
        );
        '''
        connection.execute(text(create_new_products_table))

        # Creating products table
        create_products_table = '''
        CREATE TABLE IF NOT EXISTS products (
            ID SERIAL PRIMARY KEY,
            parent_id TEXT,
            title TEXT,
            descriptions TEXT,
            main_category TEXT,
            average_rating FLOAT,
            rating_number INTEGER,
            price_euros FLOAT,
            similarity_scores FLOAT,
            new_product_title TEXT
        );
        '''
        product_data["new_product_title"] = "".join(new_product_data["title"].tolist())
        connection.execute(text(create_products_table))

        # Creating reviews table
        create_reviews_table = '''
        CREATE TABLE IF NOT EXISTS reviews (
            ID SERIAL PRIMARY KEY,
            title TEXT,
            parent_id TEXT,
            emotion TEXT,
            emotion_score FLOAT,
            rating FLOAT,
            text TEXT,
            user_id TEXT,
            verified_purchase INTEGER
        );
        '''
        connection.execute(text(create_reviews_table))

        # Inserting data using Pandas to_sql
        new_product_data.to_sql('new_products', engine, if_exists='append', index=False)
        product_data.to_sql('products', engine, if_exists='append', index=False)
        review_data.to_sql('reviews', engine, if_exists='append', index=False)

    except Exception as error:
        print('Error occurred -', error)
    finally:
        engine.dispose()
        print('PostgreSQL connection closed')





