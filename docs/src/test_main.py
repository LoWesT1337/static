import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_extract_title_simple(self):
        assert extract_title("# Hello") == "Hello"

    def test_extract_title_stripped(self):
        assert extract_title("#   My Title  ") == "My Title"

    def test_extract_title_no_h1(self):
        try:
            extract_title("## Not H1\nSome content")
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_extract_title_first_line_used(self):
        md = """# First
    # Second"""
        assert extract_title(md) == "First"
