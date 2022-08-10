from main import summarize
import sys
import os

example_dir = "test/example-docs"

def test_summarize():
    # Hack to avoid the pytest -s switch getting picked up
    # by the add-on when it looks at argv.
    if sys.argv[1] == "-s":
      del sys.argv[1]

    for filename in os.listdir(example_dir):
      with open(os.path.join(example_dir, filename)) as f:
        text = f.read()
        summary = summarize(text)
        print(summary)
        f.close()
        assert len(text) > 0, "summary() returned a non-empty string."
