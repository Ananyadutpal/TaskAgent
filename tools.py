"""Tools the agent can use. Each one is a normal Python function that returns a string."""
import ast
import datetime
import operator
import os

NOTES_DIR = "notes"
OUTPUT_DIR = "output"


def list_notes():
    """List the available note files."""
    files = sorted(os.listdir(NOTES_DIR))
    return "\n".join(files) if files else "No notes found."


def read_note(filename):
    """Read one note file."""
    path = os.path.join(NOTES_DIR, os.path.basename(filename))  # basename = no ../ tricks
    if not os.path.exists(path):
        return f"Error: {filename} not found. Use list_notes to see the files."
    with open(path, encoding="utf-8") as f:
        return f.read()


# Calculator: uses ast instead of eval() so only simple math is allowed
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _calc(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_calc(node.left), _calc(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_calc(node.operand))
    raise ValueError("unsupported expression")


def calculator(expression):
    """Evaluate a math expression like '450 + 380 + 520'."""
    try:
        return str(_calc(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: could not calculate '{expression}' ({e})"


def get_date():
    """Today's date."""
    return datetime.date.today().isoformat()


def save_report(filename, content):
    """Save text to a file inside output/."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, os.path.basename(filename))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved to {path}"


# Descriptions the model reads to decide which tool to call
TOOL_SCHEMAS = [
    {"name": "list_notes", "description": "List all note files available.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "read_note", "description": "Read the contents of a note file.",
     "input_schema": {"type": "object",
                      "properties": {"filename": {"type": "string"}},
                      "required": ["filename"]}},
    {"name": "calculator", "description": "Do math. Use this instead of calculating yourself.",
     "input_schema": {"type": "object",
                      "properties": {"expression": {"type": "string", "description": "e.g. 450 + 380"}},
                      "required": ["expression"]}},
    {"name": "get_date", "description": "Get today's date.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "save_report", "description": "Save a text report to a file.",
     "input_schema": {"type": "object",
                      "properties": {"filename": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["filename", "content"]}},
]

TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "calculator": calculator,
    "get_date": get_date,
    "save_report": save_report,
}
