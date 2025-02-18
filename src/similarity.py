'''
This script contains two functions, one to load the paraphrase-MiniLM-L6-v2 model and another one to
compare two texts and see how similar they are.
'''
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def load_similarity_model():
    '''
    Load paraphrase-MiniLM-L6-v2 model
    :return:
    paraphrase-MiniLM-L6-v2 model
    '''
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")

def compare_texts(reference_embedding, description, model):
    '''
    Compute cosine similarity between two texts.
    :param reference_embedding: Embedded text that will be compared with description.
    :param description: Text that will be compared with reference_embedding, it does not need to be embedded.
    :param model: Any SentenceTransformer model capable of embedding a text.
    :return:
    float ---- cosine similarity.
    '''
    # If there is no description there is nothing to compare.
    if description == "":
        return -1
    # Embedding description
    embedding = model.encode(description)
    # Computing cosine similarity
    similarity_scores = cosine_similarity([reference_embedding], [embedding])[0][0]

    return similarity_scores