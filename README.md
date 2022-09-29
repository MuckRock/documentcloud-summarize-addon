# DocumentCloud Summarize Add-On

This is an [add-on](https://www.documentcloud.org/help/add-ons/) for DocumentCloud that generates summaries for the documents given to it. It's a work in progress; pull requests and comments are welcome.

# Setup

From the project root directory:

- Set up a virtual environment with `python3.9 -m venv venv`.
- Create a `.env` file with Put `NLTK_DATA=nltk_data` in it.
- Put your DocumentCloud credentials in `.env` as `USER` and `PASSWORD`. (Keep your `.env` safe.)
- Run `venv/bin/pip install -r requirements.txt`.
- Run `make install-nltk`.
- To run the local server: `pip install -U flask`, then `flask run`.

# Testing

Here's how you can test this add-on locally.

- Set up a venv: `python3.9 -m venv venv` then `source venv/bin/activate`.
- Install `pytest`: `pip install -U pytest`.
- Install the production dependencies: `pip install -r requirements.txt`.
- Try running it locally: `python tools/try-summarize.py`.
  - Look at the stdout output of the test in the terminal to make sure that the summary looks reasonable.

# How it works

Here are the steps the add-on executes when summarizing:

- The text is broken up into sentences.
- Each sentence is encoded into an embedding (a vector) via the [Universal Sentence Encoder](https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder).
- The embeddings are put into [K-means clusters](https://en.wikipedia.org/wiki/K-means_clustering).
- The nearest neighbor embeddings to the centroids are collected.
- Some neighbor embeddings are filtered out if they correspond to sentences that have indicators that they may be garbage.
- The sentences corresponding to the remaining embeddings are formatted and returned as the summary.

The `summarize` function does the actual summarization, while `Summarize.main` handles getting the text out of the DocumentCloud documents, putting the summaries in a file, and uploading that file to DocumentCloud for the user to read.
