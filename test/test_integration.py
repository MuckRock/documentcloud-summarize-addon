from main import Summarize
import sys

# This is sort of more of a runner than a test for now.
def test_summarize():
    # Hack to avoid the pytest -s switch getting picked up
    # by the add-on when it looks at argv.
    if sys.argv[1] == "-s":
      del sys.argv[1]
    print(f"argv: {sys.argv}")

    summarize = Summarize()
    summarize.main(1)
    assert False, "Add-on main() completed."
