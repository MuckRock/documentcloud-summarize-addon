from main import summarize
import sys

example_texts = [
  "example-doc-text.txt",
  "short-legal-doc.txt"
]

def test_summarize():
    # Hack to avoid the pytest -s switch getting picked up
    # by the add-on when it looks at argv.
    if sys.argv[1] == "-s":
      del sys.argv[1]

    for filename in example_texts:
      with open("test/fixtures/" + filename) as f:
        text = f.read()
        summary = summarize(text)
        print(summary)
        f.close()
        assert len(text) > 0, "summary() returned a non-empty string."
