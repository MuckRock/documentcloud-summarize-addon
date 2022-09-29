import pdb
import math
import numpy as np
from annoy import AnnoyIndex
import spacy
import re

from dotenv import load_dotenv
load_dotenv()
import nltk
from nltk.cluster import KMeansClusterer, cosine_distance

nlp = spacy.load('en_use_lg')

#nlp.add_pipe('universal_sentence_encoder', config={'enable_cache': False})
nlp.replace_pipe('universal_sentence_encoder', 'universal_sentence_encoder', config={'enable_cache': False})

# TODO: Use \w minus digits to cover non-English languages.
real_word_regex = re.compile(r'[a-zA-Z]+')

max_clusters = 5
min_clusters = 3
sentences_to_pick_per_cluster = 1

# TODO: Cache summaries.
def summarize(text, max_sent_words = 50, min_sent_words = 3, sentence_to_cluster_ratio = 15):
  sentence_list = nltk.sent_tokenize(text)
  sentence_list = [sent for sent in sentence_list if real_word_regex.search(sent)]
  if len(sentence_list) < 1:
    return # TODO: Raise error.

  sentence_embeddings = [get_vector(sentence) for sentence in sentence_list]
  if len(sentence_embeddings) < 1:
    return # TODO: Raise error.
  #print(sentence_embeddings)

  n_clusters = math.floor(len(sentence_embeddings)/sentence_to_cluster_ratio)
  if n_clusters < min_clusters:
    n_clusters = min_clusters
  if n_clusters > max_clusters:
    n_clusters = max_clusters

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
    t.get_nns_by_vector(centroid, sentences_to_pick_per_cluster + 4)
    for centroid in centroids
  ]
  nearest_to_centroids.sort()
  print(nearest_to_centroids)
  t.unload()
  centroid_sentence_groups = [
    [sentence_list[index] for index in index_array]
    for index_array in nearest_to_centroids
  ]
  centroid_sentences = []
  for group in centroid_sentence_groups:
    filtered_group = [sent for sent in group
      if sentence_is_good(sent, min_sent_words, max_sent_words)
    ]
    centroid_sentences.extend(filtered_group[:sentences_to_pick_per_cluster])

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

def sentence_is_good(sent, min_sent_words, max_sent_words):
  # Warning: word_tokenize will split a string like '6).' into three words.
  words = nltk.word_tokenize(sent)
  words = [word for word in words if real_word_regex.search(word)]
  word_count = len(words)
  return word_count >= min_sent_words and word_count <= max_sent_words
