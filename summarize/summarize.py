import pdb
import math
import numpy as np
from annoy import AnnoyIndex
from dotenv import load_dotenv
load_dotenv()
import nltk
import spacy
from nltk.cluster import KMeansClusterer, cosine_distance

nlp = spacy.load('en_use_lg')

#nlp.add_pipe('universal_sentence_encoder', config={'enable_cache': False})
nlp.replace_pipe('universal_sentence_encoder', 'universal_sentence_encoder', config={'enable_cache': False})

sentence_to_cluster_ratio = 40
max_clusters = 5
min_clusters = 1
sentences_to_pick_per_cluster = 1

# Can GitHub Actions actually run tensorflow stuff?

# TODO: Cache summaries.
def summarize(text, max_sent_length = 30):
  sentence_list = nltk.sent_tokenize(text)
  if len(sentence_list) < 1:
    return # TODO: Raise error.

  #sentence_embeddings = nlp(text)
  #sentence_embeddings = nlp("Given the early stage of the investigations, the report will limit itself to a presentation of the main raw data and some first preliminary conclusions and interpretations. It is backed by two reports on the finds from the cistern (see elsewhere in this volume), in line with the project’s strategy to have a balanced input of effort and staff in the excavation and finds processing laboratory.")
  sentence_embeddings = [ get_vector(sentence) for sentence in sentence_list]
  if len(sentence_embeddings) < 1:
    return # TODO: Raise error.
  #print(sentence_embeddings)
  n_clusters = math.floor(len(sentence_embeddings)/sentence_to_cluster_ratio)
  if n_clusters < min_clusters:
    n_clusters = min_clusters

  clusterer = KMeansClusterer(n_clusters, cosine_distance, repeats=2)
  clusters_for_indexes = clusterer.cluster(sentence_embeddings, True)
  print("clusters_for_indexes", clusters_for_indexes)
  centroids = clusterer.means()
  print("centroid count", len(centroids))
  print("cluster count", clusterer.num_clusters())

  vector_size = len(sentence_embeddings[0])

  t = AnnoyIndex(vector_size, 'angular')
  for i in range(len(sentence_embeddings)):
    t.add_item(i, sentence_embeddings[i])
  t.build(10)

  nearest_to_centroids = [
    t.get_nns_by_vector(centroid, sentences_to_pick_per_cluster)
    for centroid in centroids
  ]
  nearest_to_centroids.sort()
  print(nearest_to_centroids)
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
