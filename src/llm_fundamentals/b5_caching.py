import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"

url = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
document = "\n".join(pd.read_csv(url)["text"].head(3000))   # the same long prefix every time

questions = [
    "How many of these messages mention 'exchange rate'? Give a rough estimate.",
    "What is the most common problem customers describe? One sentence.",
    "Quote one message about a lost card.",
]

for i, question in enumerate(questions, start=1):
    start = time.perf_counter()
    response = client.models.generate_content(model=MODEL, contents=document + "\n\n" + question)
    seconds = time.perf_counter() - start

    usage = response.usage_metadata
    print(f"Call {i}: input {usage.prompt_token_count:,} tokens | "
          f"cached {usage.cached_content_token_count or 0:,} | {seconds:.1f} s")
    time.sleep(20)