"""A simple AI agent that uses tools to finish multi-step tasks.

Loop: ask Claude what to do -> if it wants a tool, run it -> give the result
back -> repeat until Claude gives a final answer (or we hit MAX_STEPS).
"""
import os
import sys

import anthropic
from dotenv import load_dotenv

from tools import TOOL_FUNCTIONS, TOOL_SCHEMAS

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")
MAX_STEPS = 8  # safety limit so the agent can't loop forever

SYSTEM = (
    "You are a personal assistant agent. You can read the user's notes, do math, "
    "and save reports. Use tools when you need real data - never guess numbers. "
    "Always use the calculator for math. When done, give a short final answer."
)

client = anthropic.Anthropic()


def run_agent(task):
    messages = [{"role": "user", "content": task}]

    for step in range(1, MAX_STEPS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        # no tool requested -> this is the final answer
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        # run every tool the model asked for
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  step {step}: {block.name}({block.input})")
                try:
                    output = TOOL_FUNCTIONS[block.name](**block.input)
                except Exception as e:  # let the model see the error and recover
                    output = f"Error: {e}"
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})

    return "Stopped: reached the maximum number of steps."


if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or input("Task: ")
    print("\nWorking...\n")
    print("\nAnswer:", run_agent(task))
