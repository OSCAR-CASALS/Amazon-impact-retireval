'''
Script in charge of running a data pipeline to collect and process information about products similar to a proposal
'''
import os
from src.product import preprocess_products
from src.reviews import process_reviews
from src.collect_information import get_information
from src.database import load_into_database, load_into_postgres
import argparse

if __name__ == "__main__":
    # Collecting user input
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--category", type=str, help="Main category the product belongs to",
                        required=True)
    parser.add_argument("-ti", "--title", type=str, help="Title of the product", required=True)
    parser.add_argument("-d", "--description", type=str, help="Description of the product",
                        required=True)
    parser.add_argument("-t", "--type", type=str, help='''It indicates whether
                                                       to keep the output in a postgresql database (post) or a local
                                                       sqlite database (sqlite)
                                                       ''', default="sqlite", required=True)
    parser.add_argument("-db", "--database", type=str, help='''
                                                                In case argument --type has been set to post, these
                                                                argument indicates the connection string to the 
                                                                postgreSQL database, otherwise it contains the path
                                                                where the sqlite database is or will be created.
                                                                ''', required=True
                        )

    args = parser.parse_args()
    # Saving user input in variables
    categ = args.category
    ti = args.title
    desc = args.description
    db_type = args.type
    database_location = args.database
    # Making temporal directory
    os.mkdir("TEMP")

    # Creating dataframe with products similar to the one described by the user
    products = preprocess_products(category=categ, out_directory="TEMP", user_description=desc)

    # Sentiment analysis on reviews

    reviews = process_reviews(products["parent_id"].tolist(), category=categ, out_directory="TEMP")

    # Computing various metrics on the new product based on the products similar to those.

    resulting_df = get_information(products, reviews, title=ti, description=desc,
                                   category=categ)

    # Loading data into an SQLite or Postgre database.

    if db_type == "sqlite":
        load_into_database(new_product_data=resulting_df, product_data=products, review_data=reviews,
                           database_path=database_location)
    elif db_type == "post":
        load_into_postgres(new_product_data=resulting_df, product_data=products, review_data=reviews,
                           db_connection_string=database_location)
    else:
        os.rmdir("TEMP")
        raise ValueError("Please set a correct database type: post or sqlite")

    os.rmdir("TEMP")
