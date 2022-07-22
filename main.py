"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
import os
from dotenv import load_dotenv
import heapq

load_dotenv()
print('NLTK_DATA', os.environ['NLTK_DATA'])
# .env needs to be loaded before importing nltk so that it knows
# where to look for data.
import nltk

stopwords = nltk.corpus.stopwords.words('english')

# https://stackabuse.com/text-summarization-with-nltk-in-python/
def summarize(doc):
  sentence_list = nltk.sent_tokenize(doc.full_text)

  word_frequencies = {}
  for word in nltk.word_tokenize(doc.full_text):
    if word not in stopwords:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1

  maximum_frequency = max(word_frequencies.values())

  for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

  sentence_scores = {}
  for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
      if word in word_frequencies.keys():
        if len(sent.split(' ')) < 30:
          if sent not in sentence_scores.keys():
            sentence_scores[sent] = word_frequencies[word]
          else:
            sentence_scores[sent] += word_frequencies[word]

  summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
  summary = ' '.join(summary_sentences)

  return summary

class Summarize(AddOn):
    """A document summarization Add-On for DocumentCloud."""

    def add_summary(self, document):
        with open(f"{document.asset_url}.txt", "w+") as file_:
            summary = summarize(document)
            file_.write(summary)
            self.set_message(f"Summarized {document.asset_url}.")
            self.upload_file(file_)

    def main(self):
        """The main add-on functionality goes here."""
        self.set_message("Starting summarization.")

        doc_list = self.documents
        if not doc_list:
            if self.query:
                doc_list = self.client.documents.search(self.query)[:3]
            else:
                raise Exception("No documents found to summarize.")

        for document in doc_list:
            self.add_summary(document)

        self.set_message("Summarization complete.")
        self.send_mail(
          "Summarize", f"We summarized: {', '.join([doc.title for doc in doc_list])}")

if __name__ == "__main__":
    Summarize().main()
