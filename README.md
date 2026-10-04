# Task Agent with Tool Use

A small AI agent built with the Claude API. Instead of just answering, it decides
which tools to use, runs them, looks at the results, and keeps going until the
task is done.

## How it works
1. The user gives a task.
2. Claude decides if it needs a tool (read a note, calculate, save a file...).
3. The program runs the tool and sends the result back to Claude.
4. This repeats until Claude gives a final answer (max 8 steps).

## Tools
| Tool | What it does |
|---|---|
| `list_notes` / `read_note` | Browse and read files in `notes/` |
| `calculator` | Safe math (uses `ast`, not `eval`) |
| `get_date` | Today's date |
| `save_report` | Write a report to `output/` |

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env        # add your ANTHROPIC_API_KEY
python test_tools.py        # test the tools (no API key needed)
python agent.py "your task"
```

## Example tasks
- `python agent.py "How much did I spend on food in September, and am I within budget?"`
- `python agent.py "What are my deadlines? Save them as a report called deadlines.txt"`
- `python agent.py "Summarise my meeting notes and list what I need to do"`

## Safety
- Step limit stops infinite loops
- Calculator rejects anything except basic math
- File tools only touch `notes/` and `output/`
- Tool errors are returned to the model so it can try again

## Ideas to improve
- Add web search or a calendar tool
- Add memory across conversations
- Ask the user for confirmation before saving files
