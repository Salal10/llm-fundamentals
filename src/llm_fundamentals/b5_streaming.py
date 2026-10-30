import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash-lite"
prompt = "Explain in about 200 words how a bank decides whether to approve a personal loan."

# 1. Normal: wait for the whole answer
start = time.perf_counter()
client.models.generate_content(model=MODEL, contents=prompt)
print(f"Normal:    nothing visible for {time.perf_counter() - start:.2f} s, then the full answer\n")

time.sleep(5)

# 2. Streaming: print each piece as it arrives
start = time.perf_counter()
first_chunk_time = None
for chunk in client.models.generate_content_stream(model=MODEL, contents=prompt):
    if first_chunk_time is None:
        first_chunk_time = time.perf_counter() - start
    print(chunk.text, end="", flush=True)
total = time.perf_counter() - start

print(f"\n\nStreaming: first text after {first_chunk_time:.2f} s, complete after {total:.2f} s")    