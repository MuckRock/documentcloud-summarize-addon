"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
import os
from summarize import summarize

class Summarize(AddOn):
    """A document summarization Add-On for DocumentCloud."""

    def add_summary(self, document, file_):
        print(f"Summarizing: {document.title}\n{document.canonical_url}\n\n")
        summary = summarize(document.full_text)
        file_.write(f"{document.title}\n{document.canonical_url}\n\n{summary}\n\n")
        self.set_message(f"Summarized {document.canonical_url}.")
        return summary

    def main(self, doc_limit = 100):
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
