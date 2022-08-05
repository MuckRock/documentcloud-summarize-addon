"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
import os
import heapq
from dotenv import load_dotenv

load_dotenv()
print('NLTK_DATA', os.environ['NLTK_DATA'])
# .env needs to be loaded before importing nltk so that it knows
# where to look for data.
import nltk

stopwords = nltk.corpus.stopwords.words('english')

# https://stackabuse.com/text-summarization-with-nltk-in-python/
# https://towardsdatascience.com/simple-text-summarization-in-python-bdf58bfee77f
def summarize(text, max_sent_length = 30):
  print("Calculating word frequencies.")
  word_frequencies = {}
  word_counts = {}
  max_count = 1

  for word in nltk.word_tokenize(text):
    word = word.lower()
    if word not in stopwords:
      if word in word_counts:
        word_counts[word] += 1
      else:
        word_counts[word] = 1
      if word_counts[word] > max_count:
        max_count = word_counts[word]

  for word in word_counts:
    word_frequencies[word] = (word_counts[word]/max_count)

  print("Scoring sentences.")
  sentence_list = nltk.sent_tokenize(text)

  sentence_scores = {}
  for sent in sentence_list:
    if len(sent.split(' ')) > max_sent_length:
      continue
    for word in nltk.word_tokenize(sent.lower()):
      if word in word_frequencies:
        if sent in sentence_scores:
          sentence_scores[sent] = sentence_scores[sent] + word_frequencies[word]
        else:
          sentence_scores[sent] = word_frequencies[word]

  summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
  summary_sentences = [
    sent.replace("\n", " ").replace("  ", " ").strip() for sent in summary_sentences
  ]
  summary_sentences = [
    "• " + sent + "\n" for sent in summary_sentences
  ]
  summary = ' '.join(summary_sentences)

  print("Summary assembled.")

  return summary

class Summarize(AddOn):
    """A document summarization Add-On for DocumentCloud."""

    def add_summary(self, document, file_):
        print(f"Summarizing: {document.title}\n{document.canonical_url}\n\n")
        summary = summarize(document.full_text)
        file_.write(f"{document.title}\n{document.canonical_url}\n\n{summary}\n\n")
        self.set_message(f"Summarized {document.canonical_url}.")
        return summary

    def main(self, doc_limit = 3):
        """The main add-on functionality goes here."""
        self.set_message("Starting summarization.")

        doc_list = self.client.documents.list(id__in=self.documents)
        if not doc_list:
            if self.query:
                doc_list = self.client.documents.search(self.query)[:doc_limit]
            else:
                raise Exception("No documents found to summarize.")

        with open("summaries.txt", "w+") as file_:
          docs_summarized = 0
          for document in doc_list:
              self.add_summary(document, file_)
              docs_summarized += 1
              if docs_summarized >= doc_limit:
                  break

          self.upload_file(file_)

        self.set_message("Summarization complete.")
        self.send_mail(
          "Summarize", f"We summarized: {', '.join([doc.title for doc in doc_list])}")

if __name__ == "__main__":
    Summarize().main()
