from PyInquirer import prompt
import os


questions = [
    {
        "type": "list",
        "name": "year",
        "message": "What year is the task from?",
        "choices": [
            x for x in sorted(os.listdir(), reverse=True) if os.path.isdir(x) and not x in [".git", ".venv"]
        ],
        "default": 2,
    },
    {
        "type": "input",
        "name": "task_number",
        "message": "What is the task number?",
    },
    {
        "type": "input",
        "name": "sample_input",
        "message": "What is the sample input?",
    },
    {
        "type": "input",
        "name": "puzzle_input",
        "message": "What is the puzzle input?",
    },
]

answers = prompt(questions)

python_scaffolding = f"""from load_data import load_puzzle_input
lines = load_puzzle_input("{answers['task_number']}", sample=True)"""

with open(f"{answers['year']}/{answers['task_number']}.py", "w") as f:
    f.write(python_scaffolding)

# Create data dir if it doesn't exist
if not os.path.exists(f"{answers['year']}/data"):
    os.makedirs(f"{answers['year']}/data")

data_path = f"{answers['year']}/data/{answers['task_number']}"
os.makedirs(f"{data_path}")


# Write sample input
# Write sample input
with open(f"{data_path}/sample.txt", "w") as f:
    f.write(answers["sample_input"])

# Write puzzle input
with open(f"{data_path}/input.txt", "w") as f:
    f.write(answers["puzzle_input"])
