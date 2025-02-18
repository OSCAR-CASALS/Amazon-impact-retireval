'''

'''
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def load_roberta_classification_model():
    '''
    Load classification model Roberta
    :return:
    pipeline --- classification model
    '''
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, padding = True,
                           truncation = True, max_length = 512)

    return classifier


def classify_text_sentiment(text, classification_model):
    '''
    Use Roberta to classify the sentiments of a text into POSITIVE, NEUTRAL, and NEGATIVE.
    :param text: text that will be classified
    :param classification_model: ROBERTA pipeline.
    :return:
    dict --- A dictionary with two keys, the label asigned to argument text (label) and confidence score in set
            classification (score).
    '''
    # Dictionary with posible labels
    labels = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL",
        "LABEL_2": "POSITIVE"
    }

    # Ensure input is a list for batch processing
    is_single = isinstance(text, str)
    if is_single:
        text = [text]  # Convert single text to list

    # Apliying ROBERTA model.

    result = classification_model(text, batch_size = 32)[0]

    # Asigning the corresponding label to key "label" in the dictionary.

    return {
        "label": labels[result["label"]],
        "score": result["score"]
    }