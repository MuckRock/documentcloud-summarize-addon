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

class HelloWorld(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        name = self.data.get("name", "world")

        self.set_message("Hello World start!")

        with open("hello.txt", "w+") as file_:
            # add a hello note to the first page of each selected document
            if self.documents:
                for document in self.client.documents.list(id__in=self.documents):
                    document.annotations.create(f"Hello {name}!", 0)
                    summary = summarize(documents)
                    file_.write(summary)
                    self.set_message("Summarized a doc.")
            elif self.query:
                documents = self.client.documents.search(self.query)[:3]
                for document in documents:
                    document.annotations.create(f"Hello {name}!", 0)

            file_.write("Hello world!")
            self.upload_file(file_)

        self.set_message("Hello World end!")
        self.send_mail("Hello World!", "We finished!")


if __name__ == "__main__":
    HelloWorld().main()
