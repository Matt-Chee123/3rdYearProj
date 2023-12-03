import gensim
import nltk
from gensim.models.ldamodel import LdaModel
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

    return ' '.join(stems)

train_list = train_df['environment_statement']
preprocess_train_data = [preprocess_text(statement) for statement in train_list]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([preprocess_text(doc) for doc in preprocess_train_data])

# Finding the optimal number of clusters
silhouette_scores = []
n_samples = X.shape[0]
K = range(2, n_samples)

for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    score = silhouette_score(X, kmeans.labels_)
    silhouette_scores.append(score)

optimal_k = K[np.argmax(silhouette_scores)]
kmeans = KMeans(n_clusters=optimal_k)
kmeans.fit(X)

# Print the terms for each cluster
terms = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

for i in range(optimal_k):
    print(f"Cluster {i}:")
    for ind in order_centroids[i, :10]:  # print top-10 terms per cluster
        print(f'{terms[ind]}')
    print()