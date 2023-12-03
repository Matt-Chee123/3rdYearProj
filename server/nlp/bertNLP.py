from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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

    return ' '.join(stems)

train_list = train_df['environment_statement']
preprocess_train_data = [preprocess_text(statement) for statement in train_list]


model = SentenceTransformer('bert-base-nli-mean-tokens')

# Assume 'documents' is a list of 10 strings, where each string is a document
# Generate BERT embeddings for each document
document_embeddings = model.encode(preprocess_train_data)

# Dimensionality Reduction (Optional, depending on the size and complexity of your data)
pca = PCA(n_components=5)
document_embeddings_reduced = pca.fit_transform(document_embeddings)

# Apply clustering on the embeddings (using the reduced embeddings if PCA was applied)
num_clusters = 5  # You need to choose an appropriate number for your dataset
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(document_embeddings_reduced)
cluster_assignment = clustering_model.labels_

# Analyze clusters
for i in range(num_clusters):
    print(f"Documents in cluster {i}:")
    cluster_documents = np.where(cluster_assignment == i)[0]
    for doc_id in cluster_documents:
        print(f" - Document {doc_id}")
    print()

clustered_documents = {}

# Group documents by cluster
for doc_id, cluster_id in enumerate(cluster_assignment):
    clustered_documents.setdefault(cluster_id, []).append(preprocess_train_data[doc_id])

# Now you have `clustered_documents` defined, you can use it to extract key terms
# Define the function for extracting key terms
def extract_key_terms(texts, top_n=10):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        tfidf_scores = tfidf_matrix.sum(axis=0)
        tfidf_scores = np.squeeze(np.asarray(tfidf_scores))
        indices = tfidf_scores.argsort()[-top_n:]
        terms = vectorizer.get_feature_names_out()
        return [(terms[i], tfidf_scores[i]) for i in indices][::-1]  # highest scoring terms first
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Extract key terms for each cluster
key_terms_per_cluster = {
    cluster_id: extract_key_terms(cluster_texts)
    for cluster_id, cluster_texts in clustered_documents.items()
}

# Now you can print the key terms for each cluster
for cluster_id, key_terms in key_terms_per_cluster.items():
    print(f"Cluster {cluster_id} key terms:")
    for term, score in key_terms:
        print(f"{term} (score: {score})")
    print()