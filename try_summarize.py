from summarize.summarize import summarize
import sys
import os

example_dir = "example-docs"

for filename in os.listdir(example_dir):
  with open(os.path.join(example_dir, filename)) as f:
    text = f.read()
    summary = summarize(text)
    print(summary)
    f.close()
    assert len(text) > 0, "summary() returned a non-empty string."
