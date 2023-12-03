import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
import string
import re


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

train_df = pd.read_csv('../data/statement_training_data.csv', encoding='ISO-8859-1')

# preprocess method
def preprocess_text(text):

    #create sets for all punctuation and stop words
    punctuations = set(string.punctuation)
    stop_words = set(stopwords.words('english'))

    #tokenize
    tokens = word_tokenize(text.lower())

    #remove stopwords and punctuation using the sets
    tokens_without_stopwords = [word for word in tokens if not word.lower() in stop_words]
    tokens_without_punc = [token for token in tokens_without_stopwords if token not in punctuations]
    regex_pattern = r'\\x[a-fA-F0-9]{2}'
    tokens_without_x = [token for token in tokens_without_punc if not re.search(regex_pattern, token)]

    #lemmatization
    lemmas = [lemmatizer.lemmatize(token) for token in tokens_without_x]

    #stemming
    stems = [stemmer.stem(lemma) for lemma in lemmas]

    return stems

train_list = train_df['environment_statement']
preprocess_train_data = [preprocess_text(statement) for statement in train_list]
dictionary = corpora.Dictionary(preprocess_train_data)

print(dictionary)
# Filter out words that occur less than 20 documents, or more than 50% of the documents
dictionary.filter_extremes(no_below=2, no_above=0.5)
print(dictionary)

# Create a bag-of-words representation of the documents
corpus = [dictionary.doc2bow(doc) for doc in preprocess_train_data]

# Set parameters for LDA
num_topics = 10  # The number of topics you want to extract
passes = 10      # The number of passes through the corpus during training

# Run LDA
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)

# Print the topics found by the LDA model
for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))
    print("\n")