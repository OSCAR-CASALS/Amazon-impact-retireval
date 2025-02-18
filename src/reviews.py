'''
This script contains the function necessary to process reviews, including classifiyng them based on their positivity,
'''
import os
import wget

import pandas as pd
from src.sentiment import load_roberta_classification_model, classify_text_sentiment
import swifter

model = load_roberta_classification_model()

def process_reviews(paerent_ids, category, out_directory):
    '''
    A function in charge of selecting the reviews that belong to certain products and classify them based
    on wether they are positive, negative, or neutral. And
    :param paerent_ids:
    :param category:
    :param out_directory:
    :return:
    '''
    # Downloading review data
    url_reviews = ("https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/" +
                       category + ".jsonl.gz")

    wget.download(url_reviews, out_directory)

    # Loading review data into pandas dataframe

    data = pd.read_json(out_directory + "/" + category + ".jsonl.gz", lines=True, compression="gzip")

    # Filtering those reviews with a parent id of interest

    data = data[data["parent_asin"].isin(paerent_ids)]

    def classify_sentiments(text):
        '''
        Function that performs Sentiment classification in each thread
        :param text: text to classify
        :return:
        list --- A list of two elements, the first one corresponds to the classification of the text
                and the second one to a score of how confident the model is it classified the text correctly.
        '''
        sentiment = classify_text_sentiment(text, model)
        return [sentiment["label"], sentiment["score"]]

    # Use swifter to classify all descriptions using multithreading
    data["review_emotion"] = data["text"].swifter.apply(classify_sentiments)

    # dividing review emotion into two columns, one with the label assifgned by classify_text_sentiment and the
    # other with the score assigned to the classification.

    data["emotion"] = data["review_emotion"].str[0]
    data["emotion_score"] = data["review_emotion"].str[1]

    # Removing column review_emotion since it is redundant.
    data.drop("review_emotion", axis=1, inplace=True)

    # Remove downloaded json line

    os.remove(out_directory + "/" + category + ".jsonl.gz")

    # Selecting only columns of interest

    data = data[["parent_asin", "title", "emotion", "emotion_score", "rating", "text", "user_id",
                 "verified_purchase"]]

    # Renaming parent_asin so the name makes more sense

    data.rename(columns={"parent_asin": "parent_id"}, inplace=True)

    return data