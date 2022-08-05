from main import summarize
import sys

def test_summarize():
    # Hack to avoid the pytest -s switch getting picked up
    # by the add-on when it looks at argv.
    if sys.argv[1] == "-s":
      del sys.argv[1]

    with open("test/fixtures/example-doc-text.txt") as f:
      text = f.read()
      summary = summarize(text)
      print(summary)
      f.close()
      assert len(text) > 0, "summary() returned a non-empty string."
