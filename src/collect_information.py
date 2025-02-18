'''

'''

import pandas as pd

def get_information(product_dataframe, review_dataframe, title, description, category):
    '''
    Summerize product and review information for a proposal into a dataframe of 1 row
    :param product_dataframe: product DataFram just as outputed by preprocess_products
    :param review_dataframe: review DataFrame just as outputed by process_reviews
    :param title: string with the title of the string
    :param description: description of the proposal
    :param category: category to which the proposal belongs to
    :return:
    dataFrame ---- Single row pandas DataFrame with summerised information about products similar to the proposal.
    '''
    # Creating datframe
    df = pd.DataFrame(index=[0])
    # Adding variables defined by user in datframe
    df["title"] = title
    df["description"] = description
    df["category"] = category
    # Counting ammount of positive, neutral and negative reviews
    count_emotions = review_dataframe["emotion"].value_counts()
    df["positive_reviews"] = count_emotions.get("POSITIVE", 0)
    df["neutral_reviews"] = count_emotions.get("NEUTRAL", 0)
    df["negative_reviews"] = count_emotions.get("NEGATIVE", 0)
    # Computing average price
    df["average_price"] = product_dataframe["price_euros"].mean()
    # Seting average ratings
    df["average_rating"] = product_dataframe["average_rating"].mean()
    df["average_review_rating"] = review_dataframe["rating"].mean()
    # Counting verified purchases
    df["amount_of_verified_purchases"] = review_dataframe["verified_purchase"].sum()
    # Quantity of ratings
    df["rating_number"] = product_dataframe["rating_number"].sum()
    # Review number is the number of rows in the review dataframe
    df["review_number"] = len(review_dataframe)
    # Saving unique parent IDs.
    df["parent_ids"] = ", ".join(product_dataframe["parent_id"].unique().tolist())

    return df