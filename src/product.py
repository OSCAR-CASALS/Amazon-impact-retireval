'''
A function to extract product information, select those similar to the one described by the user, and convert prices
from US dolars to Euros.
'''

import os

import wget
import swifter

from src.similarity import load_similarity_model, compare_texts

import pandas as pd
from currency_converter import CurrencyConverter

model = load_similarity_model()

def process_description(desc):
    '''
    If description is not an empty list join all elements in a string.
    :param desc: list of strings describing a product.
    :return:
    str --- description list in string format.
    '''
    if not desc:
        return ""

    return '. '.join(desc)

def preprocess_products(category, out_directory, user_description,threshold = 0.7):
    '''
    A function to extract product information, select those similar to the one described by the user, and convert
    prices from US dolars to Euros.
    :param category: Category in string format where to look for products
    :param out_directory: Directory were metadata json lines will be stored temporarily.
    :param user_description: Filtered products must have a description similar to this string.
    :param threshold: threshold of similarity in float format.
    :return:
    DataFrame ---- dataframe with all product information processed and filter.
    '''
    # Building review and metadata download urls.
    url_metadata = ("https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_" +
                    category + ".jsonl.gz")

    # Downloading files
    wget.download(url_metadata, out_directory)
    # Read Json line into a pandas dataframe
    data = pd.read_json(out_directory + "/meta_" + category + ".jsonl.gz", lines=True, compression="gzip")
    # Processing descriptions using multithreading.
    data["string_descriptions"] = data["description"].swifter.apply(process_description)

    # Remove empty descriptions
    data = data[(data["string_descriptions"] != "") & (data["string_descriptions"] != " ")]

    # Embed user description.
    reference_embeding = model.encode(user_description)
    def check_similarity(text):
        '''
        Compute cosine similarity between text and user_description
        :param text: string with text that will be compared to user_description.
        :return:
        float ----- cosine similarity
        '''
        return compare_texts(reference_embeding, text, model)

    # Compute cosine similarity between user_description and the diferent product descriptions using multithreading.
    data["similarity_scores"] = data["string_descriptions"].swifter.apply(check_similarity)

    # Remove descriptions below a certain similarity score

    data = data[data["similarity_scores"] >= threshold]

    # Converting price from US dolars to Euros
    c = CurrencyConverter()

    def to_euros_converter(dolars):
        '''
        Convert US Dolars to Euro
        :param dolars: dolars in float format
        :return:
        float ---- Euro equivalent to argument dolars
        '''
        return c.convert(dolars, 'USD', 'EUR')

    # Convert from dolars to Euros using multithreading
    data["price_euros"] = data["price"].swifter.apply(to_euros_converter)

    # Removing json files since they are no longer needed
    os.remove(out_directory + "/meta_" + category + ".jsonl.gz")

    # Selecting only required columns
    data = data[["main_category", "title", "average_rating", "rating_number", "price_euros",
          "parent_asin", "string_descriptions", "similarity_scores"]]

    # Changing some column names to more comprensive ones.

    data.rename(columns = {"parent_asin": "parent_id", "string_descriptions": "descriptions"}, inplace = True)

    return data







