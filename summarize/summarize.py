import pdb
import math
from sklearn.cluster import KMeans
import numpy as np
from annoy import AnnoyIndex
from dotenv import load_dotenv
load_dotenv()
import nltk
import spacy
nlp = spacy.load('en_use_lg')

#nlp.add_pipe('universal_sentence_encoder', config={'enable_cache': False})
nlp.replace_pipe('universal_sentence_encoder', 'universal_sentence_encoder', config={'enable_cache': False})

# Can GitHub Actions actually run tensorflow stuff?

sentence_to_cluster_ratio = 40
max_clusters = 5
min_clusters = 1

def summarize(text, max_sent_length = 30):
  sentence_list = nltk.sent_tokenize(text)
  if len(sentence_list) < 1:
    return # TODO: Raise error.

  #sentence_embeddings = nlp(text)
  #sentence_embeddings = nlp("Given the early stage of the investigations, the report will limit itself to a presentation of the main raw data and some first preliminary conclusions and interpretations. It is backed by two reports on the finds from the cistern (see elsewhere in this volume), in line with the project’s strategy to have a balanced input of effort and staff in the excavation and finds processing laboratory.")
  sentence_embeddings = [ get_vector(sentence) for sentence in sentence_list]
  if len(sentence_embeddings) < 1:
    return # TODO: Raise error.
  #print(sentence_embeddings[3])
  n_clusters = math.floor(len(sentence_embeddings)/sentence_to_cluster_ratio)
  if n_clusters < min_clusters:
    n_clusters = min_clusters
  if n_clusters > max_clusters:
    n_clusters = max_clusters

  # sklearn kmeans uses only Euclidean distance as its metric. However, with normalized
  # vectors, Euclidean has similar results to angular distance.
  kmeans = KMeans(random_state=0, n_clusters=n_clusters).fit(sentence_embeddings)
  #print("cluster_centers_", kmeans.cluster_centers_)

  vector_size = len(sentence_embeddings[0])

  t = AnnoyIndex(vector_size, 'euclidean')
  for i in range(len(sentence_embeddings)):
    t.add_item(i, sentence_embeddings[i])
  t.build(10)
  nearest_to_centroids = [t.get_nns_by_vector(centroid, 1) for centroid in kmeans.cluster_centers_]
  nearest_to_centroids.sort()
  #print(nearest_to_centroids)
  t.unload()

  centroid_sentences = [
    sentence_list[index] for array in nearest_to_centroids for index in array
  ]

  summary_sentences = [
    sent.replace("\n", " ").replace("  ", " ").strip() for sent in centroid_sentences
  ]
  summary_sentences = [
    "• " + sent + "\n" for sent in summary_sentences
  ]
  summary = ' '.join(summary_sentences)
  print("Summary assembled.")
  return summary

def get_vector(sentence):
  embedding = nlp(sentence)
  try:
    return embedding.vector
  except:
    return
