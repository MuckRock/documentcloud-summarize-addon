# DocumentCloud Summarize Add-On

This is an [add-on](https://www.documentcloud.org/help/add-ons/) for DocumentCloud that generates summaries for the documents given to it. It's a work in progress; pull requests and comments are welcome.

# Setup

From the project root directory:

- Set up a virtual environment with `python3.9 -m venv venv`.
- Create a `.env` file with Put `NLTK_DATA=nltk_data` in it.
- Put your DocumentCloud credentials in `.env` as `USER` and `PASSWORD`. (Keep your `.env` safe.)
- Run `venv/bin/pip install -r requirements.text`.
- Run `make install-nltk`.

# Testing

Here's how you can test this add-on locally.

- Set up a venv: `python3.9 -m venv venv` then `source venv/bin/activate`.
- Install `pytest`: `pip install -U pytest`.
- Install the production dependencies: `pip install -r requirements.txt`.
- Try running it locally: `python tools/try-summarize.py`.
  - Look at the stdout output of the test in the terminal to make sure that the summary looks reasonable.

# How it works

The code is in `main.py` and implements a strategy for text summarization described in these two articles, with some additional filtering to remove likely noise:

https://stackabuse.com/text-summarization-with-nltk-in-python/
https://towardsdatascience.com/simple-text-summarization-in-python-bdf58bfee77f

Here are the steps the add-on executes when summarizing:

- The text is broken up into words.
- The frequency of each word in the text is calculated.
    - Words unlikely to be "real" words (words that are stopwords or are without alphanumeric characters or other indicators) are ignored.
- The text is broken up into sentences.
- Each sentence is scored by the total frequency of the words in it.
  - Sentences with too many words to be likely to be a real sentence (possibly a misparsing by NLTK) are ignored.
- The five sentences with the highest scores are selected.
- The sentences are formatted and returned as the summary.

The `summarize` function does the actual summarization, while `Summarize.main` handles getting the text out of the DocumentCloud documents, putting the summaries in a file, and uploading that file to DocumentCloud for the user to read.
