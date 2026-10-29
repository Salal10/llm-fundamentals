import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.1-flash-lite"

# The haystack: 3,000 real customer messages joined together
url = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
messages = pd.read_csv(url)["text"].head(3000).tolist()

needle = "IMPORTANT: the secret account code is PEARL-4471."
question = "\n\nWhat is the secret account code? Reply with the code only."

positions = {"start": 0, "middle": len(messages) // 2, "end": len(messages)}

for name, index in positions.items():
    haystack = messages[:index] + [needle] + messages[index:]
    prompt = "\n".join(haystack) + question

    start = time.perf_counter()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    seconds = time.perf_counter() - start

    print(f"{name:6} | answer: {response.text.strip():12} | "
          f"input tokens: {response.usage_metadata.prompt_token_count:,} | {seconds:.1f} s")