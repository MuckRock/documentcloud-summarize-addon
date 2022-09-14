import os
from collections import defaultdict
from dotenv import load_dotenv
import spacy
nlp = spacy.load('en_use_lg')
#nlp.add_pipe('universal_sentence_encoder', config={'enable_cache': False})
nlp.replace_pipe('universal_sentence_encoder', 'universal_sentence_encoder', config={'enable_cache': False})

# Can GitHub Actions actually run tensorflow stuff?

# https://stackabuse.com/text-summarization-with-nltk-in-python/
# https://towardsdatascience.com/simple-text-summarization-in-python-bdf58bfee77f
def summarize(text, max_sent_length = 30):
  #sentence_embeddings = nlp(text)
  sentence_embeddings = nlp("Given the early stage of the investigations, the report will limit itself to a presentation of the main raw data and some first preliminary conclusions and interpretations. It is backed by two reports on the finds from the cistern (see elsewhere in this volume), in line with the project’s strategy to have a balanced input of effort and staff in the excavation and finds processing laboratory.")
  print(sentence_embeddings.vector.shape)
  print(sentence_embeddings.vector)
  #summary_sentences = [
    #sent.replace("\n", " ").replace("  ", " ").strip() for sent in summary_sentences
  #]
  #summary_sentences = [
    #"• " + sent + "\n" for sent in summary_sentences
  #]
  #summary = ' '.join(summary_sentences)

  print("Summary assembled.")
