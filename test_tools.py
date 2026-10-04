"""Tests for the tools (no API key needed).  Run: python test_tools.py"""
from tools import calculator, read_note, list_notes, save_report

assert calculator("450 + 380 + 520") == "1350"
assert calculator("10 / 4") == "2.5"
assert calculator("-5 * 3") == "-15"
assert calculator("__import__('os')").startswith("Error")   # unsafe input is rejected
assert "expenses.txt" in list_notes()
assert "food" in read_note("expenses.txt")
assert read_note("missing.txt").startswith("Error")
assert "../" not in save_report("../test.txt", "hi")          # can't write outside output/

print("All tests passed")
