import time
from dotenv import load_dotenv
from google import genai
from datasets import load_dataset

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"
REFUSAL = "NOT IN CONTEXT"

# 20 answerable + 20 unanswerable questions from SQuAD 2.0
squad = load_dataset("rajpurkar/squad_v2", split="validation").shuffle(seed=42)
answerable = [row for row in squad.select(range(300)) if row["answers"]["text"]][:20]
unanswerable = [row for row in squad.select(range(300)) if not row["answers"]["text"]][:20]

NAIVE = "Context:\n{context}\n\nQuestion: {question}\nAnswer briefly."
GROUNDED = ("Answer using ONLY the context below. If the context does not contain the answer, "
            f"reply exactly: {REFUSAL}\n\nContext:\n{{context}}\n\nQuestion: {{question}}\nAnswer briefly.")

def ask(prompt):
    for attempt in range(4):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt).text.strip()
        except Exception:
            time.sleep(20)
    return "ERROR"

for name, template in [("NAIVE", NAIVE), ("GROUNDED", GROUNDED)]:
    hallucinated, wrongly_refused, correct = 0, 0, 0

    for row in unanswerable:
        answer = ask(template.format(context=row["context"], question=row["question"]))
        if REFUSAL not in answer:
            hallucinated += 1
            print(f"  [{name}] made up: {row['question'][:60]} -> {answer[:60]}")
        time.sleep(4)

    for row in answerable:
        answer = ask(template.format(context=row["context"], question=row["question"]))
        if REFUSAL in answer:
            wrongly_refused += 1
        elif any(gold.lower() in answer.lower() for gold in row["answers"]["text"]):
            correct += 1
        time.sleep(4)

    print(f"\n{name}: answered {hallucinated}/20 unanswerable questions, "
          f"refused {wrongly_refused}/20 answerable ones, correct on {correct}/20 answerable\n")