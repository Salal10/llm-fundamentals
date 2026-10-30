import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

questions = [
    ("A customer has $1,200. They pay rent of $450, receive a salary of $2,300, then move 15% "
     "of the new balance to savings. How much is left in the checking account?", ["2592.5"]),
    ("A $10,000 loan has 6% simple interest per year. After 18 months the borrower repays $4,000. "
     "How much is still owed?", ["6900"]),
    ("1 USD = 278 PKR. Ali sends 150 USD and the bank takes a 2% fee from the USD amount before "
     "converting. How many PKR arrive?", ["40866"]),
    ("A transfer is sent on a Thursday and takes 3 business days. On which weekday does it arrive?",
     ["tuesday"]),
    ("Account A has twice as much as account B. Account C has $500 less than A. Together they hold "
     "$4,500. How much is in account B?", ["1000"]),
]

DIRECT = "{q}\nReply with the final answer only."
STEP_BY_STEP = "{q}\nThink step by step. Then write the final answer on the last line as: ANSWER: <answer>"

def ask(prompt):
    for _ in range(4):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt)
        except Exception:
            time.sleep(20)

def is_correct(text, expected):
    last_line = text.strip().splitlines()[-1]
    cleaned = last_line.lower().replace(",", "").replace("$", "").replace(".00", "")
    return any(e in cleaned for e in expected)

for name, template in [("DIRECT", DIRECT), ("STEP BY STEP", STEP_BY_STEP)]:
    correct, output_tokens = 0, 0
    for question, expected in questions:
        for _ in range(3):
            response = ask(template.format(q=question))
            correct += is_correct(response.text, expected)
            output_tokens += response.usage_metadata.candidates_token_count
            time.sleep(4)
    print(f"{name:13} | correct: {correct}/15 | avg output tokens: {output_tokens / 15:.0f}")